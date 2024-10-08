"""
're'는 로그 라인에서 정보를 추출하는 데 사용됩니다.
'sys'는 스크립트 실행 중 오류 처리나 종료에 사용될 수 있습니다.
'datetime'은 로그의 타임스탬프를 파싱하고 조작하는 데 사용됩니다.
'deque'는 효율적으로 로그 항목을 저장하고 관리하는 데 사용될 수 있습니다.
"""
import re   # 정규표현식 모듈인 're' : 문자열 패턴 매칭과 처리에 사용
import sys  # 시스템 관련 파라미터와 함수를 제공하는 'sys' 모듈 - 스크립트 종료나 명령줄 인수 처리 등에 사용
from datetime import datetime  # 'datetime' 모듈에서 'datetime' 클래스 - 이 클래스는 날짜와 시간을 다루는 데 사용
from collections import deque  # 'collections' 모듈에서 'deque'(double-ended queue) 클래스 - deque는 양쪽 끝에서 빠르게 요소를 추가하거나 제거할 수 있는 리스트 형태의 컨테이너


def parse_log_file(file_path, num_lines):
    # 2024-08-05T23:27:41+0900
    # T 문자로 split 하기 ->
    #  2024-08-05 -> - 문자로 split하면 연월일로 분리
    #  23:27:41+0900
    # \d{4}

    # 패턴은 특정 형식의 문자열을 설명하는 문자열
    # 이 패턴은 타임스탬프, 로그 수준, 로그 메시지를 매칭하는 정규 표현식
    # 파이썬에서 문자열 앞에 r(=raw string)을 붙이면, 그 문자열이 **원시 문자열(raw string)**로 처리
    # 예를 들어 \d는 숫자를 의미. 만약 r을 붙이지 않으면 파이썬은 백슬래시를 특수 문자로 해석하려고 하기 때문에
    # \w+: 하나 이상의 문자(알파벳, 숫자, 밑줄)를 의미
    # .+: 하나 이상의 모든 문자(공백 포함)를 의미
    pattern = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}) (\w+) (.+)'
    # deque=double-ended queue(양방향 큐)로, 
    # 데이터를 빠르게 추가하거나 제거할 수 있는 자료 구조
    # 리스트와 유사하지만, 양쪽 끝에서 빠르게 삽입과 삭제가 가능
    # 이 자료 구조는 특히 큐나 스택을 구현할 때 유용
    parsed_logs = deque(maxlen=num_lines)

    try:
        with open(file_path, 'r') as file:
            for line in file:
                # file에서 읽어온 한줄씩의 문자열을 정규 표현식으로 매칭하여, 타임스탬프와 로그 수준, 메시지로 분리
                match = re.match(pattern, line)
                if match:
                    timestamp_str, log_level, message = match.groups()
                    # 타임존 정보를 제거하고 파싱 (Python 3.6 이하 버전 호환성을 위해)
                    # "2024-08-05T23:27:41+0900" 형식의 내용에서 뒤 5자리 +0900제거
                    timestamp = datetime.strptime(timestamp_str[:-5], '%Y-%m-%dT%H:%M:%S')
                    parsed_logs.append({
                        'timestamp' : timestamp,
                        'log_level' : log_level,
                        'message' : message.strip()
                    })
    except FileNotFoundError:
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
        sys.exit(1)
    except PermissionError:
        print(f"오류: '{file_path}' 파일을 읽을 권한이 없습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        sys.exit(1)

    return list(parsed_logs)

def main():
    if len(sys.argv) != 3:
        print("사용법: python log_parser.py <로그_파일_경로> <읽을 라인 수>")
        sys.exit(1)
    log_file_path = sys.argv[1]
    try:
        num_lines = int(sys.argv[2])
        if num_lines <= 0:
            raise ValueError
    except ValueError:
        print("오류: 라인 수는 양의 정수여야 합니다.")
        sys.exit(1)

    parsed_logs = parse_log_file(log_file_path, num_lines)

    print(f"'{log_file_path}'에서 최근 {len(parsed_logs)}개의 로그 항목:")
    for log in parsed_logs:
        print(f"시간: {log['timestamp']}, 레벨: {log['log_level']}, 메세지: {log['message']}")

if __name__ == "__main__":
    main() 
