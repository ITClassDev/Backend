from fastapi import APIRouter, Depends
from repositories.apps import AppsRepository
from repositories.oauth_tokens import OAuthTokensRepository
from .depends import get_apps_repository, get_current_user, get_oauth_tokens_repository
from models.apps import ProvideAccessRequest
from models.oauth_tokens import OauthToken
from models.user import User
from core.security import create_oauth_access_token
import requests

router = APIRouter()


@router.get("/get_app/{app_id}")
async def get_app_info(app_id: int, apps: AppsRepository = Depends(get_apps_repository)):
    data = await apps.get_by_id(app_id)
    return data


# generate temp token to access some user endpoints with another prefix
@router.post("/provide_access")
async def provide_access(app_info: ProvideAccessRequest, current_user: User = Depends(get_current_user),
                         apps: AppsRepository = Depends(get_apps_repository),
                         tokens: OAuthTokensRepository = Depends(get_oauth_tokens_repository)):
    if current_user:
        app_config = await apps.get_by_id(app_info.app_id)
        # Expire all old tokens from this app
        # TODO
        # Optionaly add time filter(1h for example)
        await tokens.expire_all(app_info.app_id)

        access_token = create_oauth_access_token(
            current_user.id, app_info.app_id)  # generate token string
        token_object = OauthToken(token=access_token, app_id=app_info.app_id, to_user=current_user.id)
        await tokens.save_token(token_object)

        return {"status": True, "oauth_access_token": access_token,
                "redirect_to": f"{app_config.redirect_url}?access_token={access_token}"}
    else:
        return {"status": False}


@router.get("/get_user/{token}")
async def get_user(token: str, tokens: OAuthTokensRepository = Depends(get_oauth_tokens_repository)):
    token_data = await tokens.get_by_token(token)
    if token_data:
        await tokens.expire_token(token)
        return {"status": True, "user_id": token_data.to_user}
    else:
        return {"status": False, "detail": "Please provide working token"}
