from services.prompt_service import PromptService


def test_prompt_render() -> None:
    svc = PromptService()
    out = svc.render("hello {{name}}", {"name": "paper"})
    assert out == "hello paper"
