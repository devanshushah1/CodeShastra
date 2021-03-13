from django.shortcuts import render

# Create your views here.

from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.template.loader import render_to_string
import django_filters.rest_framework
from .models import *
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
import nltk
from nltk.tag import pos_tag
from nltk.corpus import wordnet
from PyDictionary import PyDictionary
nltk.download('wordnet')
# Create your views here.
f_url = 'http://localhost:3000/'

# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')


def EmailVerification(user):
    token = get_random_string(length=32)
    user.email_verified_hash = token
    user.save()
    verify_link = f_url + 'login/?token=' + token
    subject = 'Verify your email.'
    to = user.email
    html_content = render_to_string('accounts/EmailVerification.html', {
        'verify_link': verify_link,
    })
    send_mail(subject=subject, from_email='djangonotforme@gmail.com', message='abcd', recipient_list=[to],
              html_message=html_content)


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        # username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("emailid")
        firstname = request.data.get("firstname")
        phonenumber = request.data.get("phonenumber")
        state = request.data.get("state")
        district = request.data.get("district")
        if request.user:
            if password is None or email is None or firstname is None or phonenumber is None or state is None or district is None:
                return Response({'error': 'Please provide all the user information'},
                                status=status.HTTP_400_BAD_REQUEST)
            user = CustomUser.objects.filter(email=email).exists()
            if user:
                return Response({'msg': 'account with this email already exists.'})
            user = CustomUser.objects.create_user(email=email, password=password)
            user.save()
            if not user:
                return Response({'error': 'User not created'},
                                status=status.HTTP_404_NOT_FOUND)
            user.email = email
            user.first_name = firstname
            user.phone_number = phonenumber
            user.state = state
            user.district = district
            user.save()
            user_data = {
                'msg': 'Account created successfully. Please verify your email by clicking on the link sent to your email address.',
                'user': {
                    'userid': user.id,
                    # 'username': user.username,
                    'emailid': user.email,
                    'firstname': user.first_name,
                    'phonenumber': user.phone_number,
                    'state': user.state,
                    'district': user.district
                }
            }
            EmailVerification(user)
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not authorized'},
                            status=status.HTTP_400_BAD_REQUEST)


class EmailVerify(APIView):
    def post(self, request):
        token = request.data['token']
        res = {
            'status': 'success',
            'message': 'Valid'
        }

        if CustomUser.objects.filter(email_verified_hash=token, email_verified=0).exists():
            tokenExists = CustomUser.objects.get(email_verified_hash=token, email_verified=0)
            tokenExists.email_verified = 1
            tokenExists.is_active = True
            tokenExists.save()
        else:
            res = {
                'status': 'failed',
                'message': 'Invalid',
            }

        return Response(res)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class ItemViewSet(viewsets.ModelViewSet):
    model = Item
    serializer_class = ItemSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('category', 'state', 'district')

    def get_queryset(self, *args, **kwargs):
        if "keywords" in self.kwargs:
            keywords = self.request.query_params.get('keywords')
            keywords = keywords.split(',')
            print(keywords)
            return Item.objects.all()
        else:
            return Item.objects.all()

    def create(self, request, *args, **kwargs):
        item_name = request.data.get('item_name')
        brand_name = request.data.get('brand_name')
        category = request.data.get('category')
        description = request.data.get('description')
        is_found = request.data.get('is_found')
        # image = request.data.get('Image')
        state = request.data.get('state')
        district = request.data.get('district')
        # keyword = keyword.lower()
        user = request.user
        print(user)
        item = Item()
        item.item_name = item_name
        item.brand_name = brand_name
        item.description = description
        print(is_found)
        item.is_found = is_found
        print(1)
        item.posted_by=user
        print(2)
        # item.Image=image
        item.state=state
        item.district=district
        item.category=category

        item.save()


        kw_ids = []
        # keywords = keyword.split(" ")
        is_noun = lambda pos: pos[:2] == 'NN'
        is_adj = lambda pos: pos[:2] == 'JJ'
        tokenized = nltk.word_tokenize(description)
        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
        adjs = [word for (word, pos) in nltk.pos_tag(tokenized) if is_adj(pos)]
        for kw in nouns:
            obj, created = Keywords.objects.get_or_create(name=kw)
            print(created)
            # s = wordnet.synsets(kw)
            kw_ids.append(obj.id)
            s = PyDictionary()
            syn = s.synonym(kw.lower())
            print("syn", syn)
            print(0)
            if created:
                for a in syn[:20]:
                    print(1)
                    print(a)
                    objx, created = Keywords.objects.get_or_create(name=a.lower())
                    kw_ids.append(objx.id)
        for kw in adjs:
            obj, created = Keywords.objects.get_or_create(name=kw)
            print(created)
            # s = wordnet.synsets(kw)
            kw_ids.append(obj.id)
            s = PyDictionary()
            syn = s.synonym(kw.lower())
            print("syn", syn)
            print(0)
            if created:
                for a in syn[:20]:
                    print(1)
                    print(a)
                    objx, created = Keywords.objects.get_or_create(name=a.lower())
                    kw_ids.append(objx.id)
        for obj in kw_ids:
            item.keyword.add(obj)
        
        return Response({'success':'Created Successfully'}, status=status.HTTP_201_CREATED)

class ClaimView(viewsets.ModelViewSet):
    model = Claims
    serializers_class= ClaimSerializer
    queryset = Claims.objects.all()



