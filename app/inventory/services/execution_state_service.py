from datetime import datetime, UTC

from sqlalchemy.orm import Session

from app.inventory.models.monitoring_execution_state import (
    MonitoringExecutionState
)

from app.inventory.models.enums import (
    ExecutionStatus,
    ExecutionStage
)


def start_execution(
    db: Session,
    node,
    implementation
):

    state = (
        db.query(MonitoringExecutionState)
        .filter(
            MonitoringExecutionState.node_id == node.id,
            MonitoringExecutionState.implementation_id == implementation.id
        )
        .first()
    )

    #
    # Create state row first time only
    #
    if not state:

        state = MonitoringExecutionState(
            node_id=node.id,
            system_id=node.system_id,
            customer_id=node.customer_id,
            implementation_id=implementation.id
        )

        db.add(state)

    #
    # Update execution start
    #
    state.last_started_at = datetime.now(UTC)

    state.current_stage = ExecutionStage.SSH

    db.commit()
    db.refresh(state)

    return state


#SUCCESS UPDATE

def execution_success(
    db: Session,
    state,
    duration_ms,
):

    now = datetime.now(UTC)

    state.current_status = ExecutionStatus.SUCCESS

    state.current_stage = ExecutionStage.COMPLETE

    state.last_finished_at = now

    state.last_success_at = now

    state.last_duration_ms = duration_ms

    state.total_successes += 1

    state.total_executions += 1

    state.consecutive_failures = 0

    state.current_message = "Execution completed successfully"


    db.commit()
    db.refresh(state)


#FAILURE UPDATE

def execution_failed(
    db: Session,
    state,
    error
):

    now = datetime.now(UTC)

    state.current_status = ExecutionStatus.FAILED

    state.last_failure_at = now

    state.last_finished_at = now

    state.total_failures += 1

    state.total_executions += 1

    state.consecutive_failures += 1

    state.last_error_type = type(error).__name__

    state.last_error_message = str(error)

    state.current_message = str(error)


    db.commit()
    db.refresh(state)