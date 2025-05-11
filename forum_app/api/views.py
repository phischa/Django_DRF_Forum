from rest_framework import viewsets, generics, permissions
from forum_app.models import Like, Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer, LikeSerializer
from .permissions import IsOwnerOrAdmin, CustomQuestionPermission
from .throttling import QuestionThrottle, QuesttionGetThrottle, QuesttionPostThrottle

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [CustomQuestionPermission]
    throttle_classes = [QuestionThrottle]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_throttles(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [QuesttionGetThrottle()]
        
        if self.action == 'create':
            return [QuesttionPostThrottle()]
        
        return []



class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Answer.objects.all()

        """ Query Paramenter: Filter können zusammengefügt werden und ermöglichen so eine genauer Suchanfrage
        z.B. author: bob & content contains: 'Django'.
        URL: http://127.0.0.1:8000/api/forum/answers/?content=Django&author=bob  """
        content_param = self.request.query_params.get('content', None)
        if content_param is not None:
            queryset = queryset.filter(content__icontains=content_param)

        username_param = self.request.query_params.get('author', None)
        if username_param is not None:
            queryset = queryset.filter(author__username=username_param)

        return queryset

class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsOwnerOrAdmin]


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
