from django.contrib.auth import get_user_model, login
from django.http import Http404, HttpResponse
from django.views.generic import TemplateView
import requests

client_id = "82fc6577-b0c8-4cbb-82a2-c0318ff3743a"
client_secret = ""


class LoginView(TemplateView):
    template_name = "login.html"


class ActualLoginView(TemplateView):
    template_name = "auth.html"

    def dispatch(self, request, *args, **kwargs):
        data = {'grant_type': 'authorization_code', 'code': request.GET["code"], 'redirect_uri': "http://localhost:8000/auth"}
        access_token_response = requests.post("https://auth.fit.cvut.cz/oauth/token", data=data, verify=False, allow_redirects=False,
                                              auth=(client_id, client_secret))
        access_token = access_token_response.json()["access_token"]
        resp = requests.get("https://auth.fit.cvut.cz/oauth/userinfo",
                            headers={"authorization": "Bearer {}".format(access_token)})
        username = resp.json()["username"]
        maybe_user = get_user_model().objects.filter(username=username)
        if not maybe_user.exists():
            raise Http404("This user account does not exist!")
        user = maybe_user.get()
        login(request, user)
        return HttpResponse("Login successful! as {} Use HttpResponseRedirect(url) to wherever you need".format(username))
