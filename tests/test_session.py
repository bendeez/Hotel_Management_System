from utils import RequestMethod
import pytest
from pytest_lazy_fixtures import lf
from app.session.schemas import SessionsOut


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_create_chat_session(account, http_request, sessions, user_request):
    tokens, account = account
    response = await http_request(
        path="/session/session", method=RequestMethod.POST, token=tokens.access_token
    )
    assert response.status_code == 201
    data = response.json()
    session = SessionsOut(**data)
    assert session == SessionsOut(
        id=session.id,
        end_time=session.end_time,
        ip_address=session.ip_address,
        user_agent=session.user_agent,
        account_id=account.id,
    )


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_get_account_chat_logs(account, http_request, chat_logs):
    tokens, account = account
    params = {"limit": 2, "offset": 0, "order": "desc", "order_by": "end_time"}
    response = await http_request(
        path="/session/sessions",
        params=params,
        method=RequestMethod.GET,
        token=tokens.access_token,
    )
    assert response.status_code == 200
    data = response.json()
    chat_sessions = [SessionsOut(**d) for d in data]
    assert len(chat_sessions) <= params["limit"]
    assert chat_logs[0].date >= chat_logs[1].date
    assert all(session.account_id == account.id for session in chat_sessions)
