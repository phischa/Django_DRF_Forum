from rest_framework.throttling import UserRateThrottle

class QuestionThrottle(UserRateThrottle):
    scope = 'question'

#     def allow_request(self, request, view):

#         if request.method == "GET":
#             return True
        
#         now_scope = 'question-' + request.method.lower()
#         if now_scope in self.THROTTLE_RATES:
#             self.scope = now_scope
#             self.rate = self.get_rate()
#             self.num_requests, self.duration = self.parse_rate(self.rate)

#         return super().allow_request(request, view)
    
class QuesttionGetThrottle(UserRateThrottle):
    scope = 'question-get'

class QuesttionPostThrottle(UserRateThrottle):
    scope = 'question-post'