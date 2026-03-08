"""
LLM service for Deed Finance advisor.
Supports Anthropic (Claude) and OpenAI (GPT) APIs.
"""
import os


class AnthropicProvider:
    """Anthropic Claude API provider."""

    def __init__(self, api_key, model="claude-sonnet-4-20250514"):
        import anthropic
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def get_advice(self, system_prompt, user_message):
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        return response.content[0].text

    def get_advice_stream(self, system_prompt, user_message):
        with self.client.messages.stream(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        ) as stream:
            for text in stream.text_stream:
                yield text


class OpenAIProvider:
    """OpenAI GPT API provider."""

    def __init__(self, api_key, model="gpt-4o-mini"):
        import openai
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def get_advice(self, system_prompt, user_message):
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content

    def get_advice_stream(self, system_prompt, user_message):
        stream = self.client.chat.completions.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


def get_llm_provider():
    """
    Factory: return the configured LLM provider, or None if not configured.
    Reads LLM_PROVIDER and LLM_API_KEY from environment.
    """
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        return None

    provider_name = os.environ.get("LLM_PROVIDER", "anthropic").lower()

    if provider_name == "anthropic":
        return AnthropicProvider(api_key=api_key)
    elif provider_name == "openai":
        return OpenAIProvider(api_key=api_key)
    else:
        return None


SYSTEM_PROMPT = """You are a Canadian credit card rewards advisor for Deed Finance.
You help users maximize their credit card points to cover subscription costs.

You will receive the user's financial context including:
- Their credit cards with current points balances and earn rates
- Their tracked subscriptions with monthly costs
- Their spending patterns and bonus categories

Give concise, actionable advice. Focus on:
1. Which card to use for which spending category to maximize points
2. How to cover the most subscriptions with earned points
3. Spending optimizations (e.g., "shift $X of dining spend to card Y for 3x more points")
4. Whether their card lineup is optimal for their spending patterns

Keep responses under 300 words. Use dollar amounts in CAD. Be specific with card names and numbers.
Do NOT give general financial advice. Focus only on credit card points optimization."""


def build_user_context(user_cards, user_subs, spending_results=None):
    """
    Build a user context string from their financial data.
    All objects should be already loaded (not lazy-loaded).
    """
    lines = ["## Your Credit Cards"]
    for uc in user_cards:
        card = uc.credit_card
        lines.append(
            f"- {card.name} ({card.bank}): {uc.current_points:,} {card.points_name}, "
            f"base {card.base_earn_rate}x, point value {card.point_value_cents}c, "
            f"annual fee ${card.annual_fee:.0f}"
        )

    lines.append("\n## Your Subscriptions")
    total_sub_cost = 0
    for us in user_subs:
        sub = us.subscription
        lines.append(f"- {sub.name}: ${sub.monthly_cost_cad:.2f}/month ({sub.category})")
        total_sub_cost += sub.monthly_cost_cad
    lines.append(f"Total monthly subscription cost: ${total_sub_cost:.2f}")

    if spending_results:
        lines.append("\n## Recent Spending Calculation")
        for r in spending_results:
            lines.append(
                f"- {r['category']}: ${r['amount']:.2f} -> best card: {r['card']} "
                f"({r['rate']}x, {r['points']:,} pts)"
            )

    return "\n".join(lines)
