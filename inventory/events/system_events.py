from sqlalchemy import event, select, func

from inventory.models.system import System
from inventory.models.customer import Customer


@event.listens_for(System, "before_insert")
def generate_system_code(mapper, connection, target):

    # -------------------------------------------------
    # Get customer code
    # -------------------------------------------------

    customer_query = (
        select(Customer.code_name)
        .where(Customer.id == target.customer_id)
    )

    customer_code = connection.execute(
        customer_query
    ).scalar_one_or_none()

    if not customer_code:
        raise ValueError(
            f"Customer with id {target.customer_id} not found"
        )

    # ------------------------------------------
    # Get max sequence
    # ------------------------------------------

    sequence_query = (
        select(func.max(System.sequence_number))
        .where(
            System.customer_id == target.customer_id,
            System.type == target.type
        )
    )

    max_sequence = connection.execute(
        sequence_query
    ).scalar()

    next_sequence = (max_sequence or 0) + 1

    target.sequence_number = next_sequence

    # ------------------------------------------
    # Generate code
    # ------------------------------------------

    # -------------------------------------------------
    # Generate final system code
    # -------------------------------------------------

    target.system_code = (
        f"{customer_code}_"
        f"{target.type.value}_"
        f"{next_sequence:02d}"
    )