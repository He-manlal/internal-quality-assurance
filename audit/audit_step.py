from pydantic import BaseModel
from fastapi import APIRouter
from typing import Optional
from db import get_db

router = APIRouter()

class AuditStepCreate(BaseModel):
    audit_id: int
    step_name: str
    status: str
    remarks: Optional[str] = None
    is_final_step: bool = False

@router.post("/audit_step")
def create_audit_step(step: AuditStepCreate):
    conn, cursor = get_db()
    try:
        insert_query = """
        INSERT INTO audit_step (\"audit_id\", \"step_name\", \"status\", \"remarks\", \"final_step\")
        VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (step.audit_id, step.step_name, step.status, step.remarks, step.is_final_step))
        conn.commit()
        
        if step.is_final_step:
            fetch_steps_query = """
            SELECT status FROM audit_step WHERE "audit_id" = %s;
            """
            cursor.execute(fetch_steps_query, (step.audit_id,))
            statuses = cursor.fetchall()

            # Extract status list
            status_list = [row[0].lower() for row in statuses] 

            # Check if any step failed
            if "failed" in status_list:
                final_status = "failed"
            else:
                final_status = "passed"

            # Update audit table with final_status
            update_audit_query = """
            UPDATE audit SET final_status = %s WHERE audit_id = %s;
            """
            cursor.execute(update_audit_query, (final_status, step.audit_id))
            conn.commit()

   
        
        return {"message": "Audit step created successfully"}
    finally:
        cursor.close()
        conn.close()

