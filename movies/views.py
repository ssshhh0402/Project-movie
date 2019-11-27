from django.shortcuts import render,redirect,get_object_or_404
from accounts.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import get_user_model
from .models import Movie, Genre, MK, MG, Comment
from .forms import CommentForm
from IPython import embed
import datetime, requests, random


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    signupform = CustomUserCreationForm()
    loginform = AuthenticationForm()
    context = {
        'signupform': signupform,
        'loginform': loginform
    }
    return render(request, 'movies/home.html', context)

def index(request):
    User = get_user_model()
    user = get_object_or_404(User, username=request.user)
    if user.preference.all():
        now_list = recommendation_2(request.user.id)
        movie_list = []
        for idx in user.preference.all():   
            genre_movie = {}
            imsi_list = []
            movies = []
            genre_movie['genre'] = Genre.objects.get(id=idx.id).name
            result = MG.objects.filter(genre = idx.id).order_by('-popularity')
            for movie in result:
                try:
                    item = Movie.objects.get(movieid=movie.movieid)
                    movies.append(item)
                    if len(movies) == 10:
                        break
                except:
                    continue
            genre_movie['genre_movie_list'] = movies[:10]
            
            

            #movie = Movie.objects.filter(genres__contains= idx.id).order_by('-popularity')
            #embed()
            #genre_movie['genre_movie_list'] = movie[:10]
            movie_list.append(genre_movie)
        context = {
            'movie_list' : movie_list,
            'now' : now_list
        }

        return render(request, 'movies/index.html', context)
    else:
        return redirect('accounts:genre')

def detail(request, movie_pk):
    movie = get_object_or_404(Movie, movieid=movie_pk)
    genre_list = []
    movie_genre_list = eval(movie.genres)
    for genre in movie_genre_list:
        genre_item = Genre.objects.get(id=genre)
        genre_list.append(genre_item.name)
    movie.genres = genre_list
    video_list = ''
    if eval(movie.videos):
        video_list = (eval(movie.videos)[0])
    movie.videos = video_list
    movie.credit = eval(movie.credit)
    re_movie = get_re(movie_pk)
    comments = movie.comment_set.all()

    context = {
        'movie': movie,
        're_movie' : re_movie,
        'comments' : comments,
    }
    return render(request,'movies/detail.html', context)
    
def getNow():
    yesterday = datetime.date.today() - datetime.timedelta(1)
    yesterday = yesterday.strftime('%Y%m%d')
    movie_list = []
    api_key = '407e887e6e33a30edd477d217f18d883'
    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={api_key}&targetDt={yesterday}&multiMovieYn=N'
    a = requests.get(url).json()
    response = requests.get(url).json().get('boxOfficeResult').get('dailyBoxOfficeList')
    api_key = '69855813cd52f7cdbc7e336c8afaac95'
    for movie in response:
        try:
            item = Movie.objects.filter(title=movie.get('movieNm')).order_by('-release_date')
            movie_list.append(item)
        except:
            movie_title = movie.get('movieNm')
            find_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=ko-KR&query={movie_title}&page=1&include_adult=true'
            response_2 = requests.get(find_url).json().get('results')
            if response_2:
                movie_id = response_2[0].get('id')
            else:
                continue
            detail_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=ko-KR&append_to_response=videos%2Ckeywords%2Ccredits'
            response_detail = requests.get(detail_url).json()
            genre_list = []
            video_list = []
            G = len(MG.objects.all())
            for genre in response_detail.get('genres'):
                genre_list.append(genre.get('id'))
                MG.objects.create(id=G, movieid=movie_id, genre=genre.get('id'),popularity=response_detail.get('popularity'))
                G += 1

            K = len(MK.objects.all())
            for keyword in response_detail.get('keywords').get('keywords'):
                MK.objects.create(id=K, movieid=movie_id, keyword=keyword.get('id'), popularity = response_detail.get('popularity'))
                K += 1
            
            a = response_detail.get('videos').get('results')
            if a:
                for movie in a:
                    video_list.append(movie.get('key'))
            else:
                detail_url2 = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US&append_to_response=videos%2Ccredits'
                response_detail_en = requests.get(detail_url2).json()
                if response_detail_en.get('videos').get('result'):
                    for movie in response_detail_en.get('videos').get('result'):
                        video_list.append(movie.get('key'))
            movie = Movie.objects.create(movieid=response_detail.get('id'),title=response_detail.get('title'), overview=response_detail.get('overview'), genres=genre_list, poster=response_detail.get('poster_path'), original_title=response_detail.get('original_title'), popularity= response_detail.get('popularity'), runtime= response_detail.get('runtime'), release_date=response_detail.get('release_date'), videos = video_list, credit = response_detail.get('credits').get('cast'))
            movie_list.append(movie)
    return movie_list

def get_re(a):
    api_key = '69855813cd52f7cdbc7e336c8afaac95'
    url = f'https://api.themoviedb.org/3/movie/{a}/recommendations?api_key={api_key}&language=ko-KR&page=1'
    response= requests.get(url).json().get('results')
    movie_list = []
    recommendation_list = []
    if not response:                                # 추천 영화 없으면
        return recommendation_list
    # if len(response) >= 10:
    #     for i in range(10):
    #         embed()
    #         movie_list.append(response[i].get('id'))
    # else:
    #     for i in range(len(response)):
    #         movie_list.append(response[i].get('id'))
    response = response[:10]
    for i in range(len(response)):
        movie_list.append(response[i].get('id'))
        
    for movie in movie_list:
        genre_list = []
        video_list = []
        try:
            item = Movie.objects.get(movieid=movie)
            recommendation_list.append(item)
        except:
            url = f'https://api.themoviedb.org/3/movie/{movie}?api_key={api_key}&language=ko-KR&append_to_response=videos%2Ccredits'
            #response = requests.get(url).json().get('result')
            response = requests.get(url).json()
            for genre in response.get('genres'):
                genre_list.append(genre.get('id'))
            videos = response.get('videos').get('results')
            if videos:
                for video in videos:
                    video_list.append(video.get('key'))
            else:
                url_en = f'https://api.themoviedb.org/3/movie/{movie}?api_key={api_key}&language=en-US&append_to_response=videos%2Ccredits'
                response_en = requests.get(url_en).json().get('videos').get('results')
                if response_en:
                    for video in response_en:
                        video_list.append(video.get('key'))
            movie_item = Movie.objects.create(movieid=movie, title=response.get('title'), overview=response.get('overview'), genres=genre_list, poster=response.get('poster_path'), original_title=response.get('original_title'), popularity=response.get('popularity'), runtime=response.get('runtime'), release_date = response.get('release_date'),videos=video_list,credit=response.get('credits').get('cast'))
            recommendation_list.append(movie_item)
    return recommendation_list

########################################댓글#########################
@require_POST
def comment_create(request, movie_pk):                          # 여기다가 평점도 저장해야 할듯
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, movieid=movie_pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie = movie
            comment.user = request.user
            comment.save()
            num = len(movie.comment_set.all())
            movie.score = ((movie.score *(num - 1)) + comment.score) / num
            movie.save()
            return redirect('movies:detail', movie_pk)
        # 타당하지 않을 경우 Alert 창 띄우면 될것같은데...
    else:
        return HttpResponse('Unauthorized', status=401)


@require_POST   
def comment_delete(request, movie_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
########################################좋아요############################

def like(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, movieid=movie_pk)
        is_liked = True
        if request.user in movie.like_users.all():
            movie.like_users.remove(request.user)
            is_liked = False
        else:
            movie.like_users.add(request.user)
            is_liked = True
        return JsonResponse({'is_liked':is_liked})
    else:
        return redirect('/')
###########################################################################

def recommendation_2(a):
    try:
        comments = Comment.objects.filter(user=a)
    except:
        return []
    high_list = []
    highest_val = -0xffffff
    for comment in comments:
        if comment.score > highest_val:
            high_list.clear()
            high_list.append(comment.movie)
            highest_val = comment.score
        elif comment.score == highest_val:
            high_list.append(comment.movie)
    
    if not len(high_list):
        lists = (Movie.objects.all().order_by('-score','-popularity'))[:10]
        return lists
    movie = random.choice(high_list)   
    key_list = []
    keywords = eval((Movie.objects.get(movieid=movie.movieid)).keywords)
    for keyword in keywords:
        
        lists = MK.objects.filter(keyword=keyword)
        for item in lists:
            if item.movieid not in key_list:
                key_list.append(item.movieid)
    recommendation_list = Movie.objects.filter(movieid__in=key_list).order_by('-score','-popularity')
    if not recommendation_list:
        return []
    else:
        return recommendation_list[:10]

def about(request):
    return render(request, 'movies/about.html')