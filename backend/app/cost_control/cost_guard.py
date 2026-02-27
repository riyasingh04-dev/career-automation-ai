from backend.app.observability.logger import app_logger

class CostGuard:
    PRICING = {
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        "llama-3.3-70b-versatile": {"input": 0.00059, "output": 0.00079},
    }

    @staticmethod
    def track_usage(model: str, input_tokens: int, output_tokens: int):
        prices = CostGuard.PRICING.get(model, {"input": 0, "output": 0})
        cost = (input_tokens / 1000 * prices["input"]) + (output_tokens / 1000 * prices["output"])
        
        app_logger.info("usage_tracked", extra={
            "model": model,
            "tokens": input_tokens + output_tokens,
            "estimated_cost": cost
        })
        return cost

    @staticmethod
    def check_budget(user_id: int):
        # Placeholder for budget enforcement logic
        return True
