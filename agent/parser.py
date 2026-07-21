from pydantic import BaseModel, Field
from typing import Dict, Any

class AgentDecision(BaseModel):

    tool : str = Field(
        description = "Selected tool name. Use 'rag' or 'chat'."
    )

    argument : Dict[str, Any] = Field(
        default_factory = dict,
        description = "Arguments required by the selected tool."
    )