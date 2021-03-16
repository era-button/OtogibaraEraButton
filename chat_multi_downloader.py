import subprocess
import sys

member_list = [
    "ZbT8sM1VLUA",
    "ZbT8sM1VLUA"
]
#この辺りでvideokeyやタイトルをごにょごにょする。

def command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True)
        for line in result.stdout.splitlines():
            yield line
    except subprocess.CalledProcessError:
        print('Command [' + cmd + '] was failed.', file=sys.stderr)
        sys.exit(1)


def main():
    """
    main関数
    """
    for video_id in member_list:
        cmd = 'chat_downloader https://www.youtube.com/watch?v=' + video_id + ' --cookies ../cookie.txt --output "result_member/' + video_id + '.json" > result_member/' + video_id + '.txt'  # 実行するコマンド
        print(cmd)
        for result in command(cmd):
            print(result)


if __name__ == "__main__":
    main()
