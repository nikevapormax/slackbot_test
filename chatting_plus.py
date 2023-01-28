from slack_sdk import WebClient


class ChattingPlusAPI:
    def __init__(self, token):
        self.client = WebClient(token)  # 슬랙 클라이언트 인스턴스 생성 
        
    def get_channel_name(self, channel_name):
        """
        슬랙 채널ID 조회
        """
        result = self.client.conversations_list()  # 딕셔너리 형태로 들어와서 .data 를 쓸 필요는 없음
        channels = result["channels"]
        channel = list(filter(lambda c:c["name"] == channel_name, channels))[0]
        channel_id = channel["id"]
        
        return channel_id

    def get_message_ts(self, channel_id, query):
        """
        슬랙 채널 내 메세지 조회
        """
        result = self.client.conversations_history(channel=channel_id)
        messages = result["messages"]
        message = list(filter(lambda x: x["text"] == query, messages))[0]
        message_ts = message["ts"]
        
        return message_ts
    
    def post_thread_message(self, channel_id, message_ts, text):
        """
        슬랙 채널 내 메세지의 Thread에 댓글 달기
        """
        result = self.client.chat_postMessage(
            channel=channel_id,
            text = text,
            thread_ts = message_ts
        )

        return result


token = "xoxb-4736844481840-4713162860946-Ce7ZUpJnl4LWCTXfJsVq6BcJ"
channel_id = "C04LJJ3Q92T"
slack = ChattingPlusAPI(token)

channel_name = "test"
query = "테이블링"
text = "현재 회의실 예약 현황"

# 채널ID 파싱
channel_id = slack.get_channel_name(channel_name)
# 메세지ts 파싱
message_ts = slack.get_message_ts(channel_id, query)
# 댓글 달기
slack.post_thread_message(channel_id, message_ts, text)
