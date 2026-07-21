from agent.parser import AgentDecision
from services.agent_llm_service import reason
from services.environment_service import get_document_count
from agent.tools import TOOLS,chat_tool



class ReactAgent:

    def reason(self, user_input: str):

        response = reason(
            question=user_input,
            document_count=get_document_count()
        )

        decision = AgentDecision.model_validate_json(response)

        return decision

    def act(self, decision,user_input : str):

        tool = TOOLS[decision.tool]

        result = tool(
            **decision.argument
        )

        if(decision.tool=="rag" and result["answer"].strip().lower() == "not_found") :
            return chat_tool(question=user_input)

        return result

    def observe(self, result):

        return result

    def respond(self, observation):

        return observation

    def invoke(self, user_input: str):

        decision = self.reason(user_input)

        result = self.act(decision,user_input)

        observation = self.observe(result)

        response = self.respond(observation)

        return {
            ** response,
            "tool" : decision.tool,
        }
