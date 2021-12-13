from youtube_transcript_api import YouTubeTranscriptApi as YTA
from youtube_transcript_api.formatters import JSONFormatter
import pafy
import threading
def thread_function(video_id, video_num, num_videos):
    try:
            transcript = YTA.get_transcript(video_id)
            # .format_transcript(transcript) turns the transcript into a JSON string.
            json_formatted = formatter.format_transcript(transcript)
        except:
            print("no transcript for " + pafy.new(video_id).title)
            with open("noTranscipt.txt", 'a') as f:
                f.write(video_id + " " + pafy.new(video_id).title)

        #sanatize inputs
        title=""
        for c in pafy.new(video_id).title:
            if c.isalnum() or c == " ":
                title += c


        # Now we can write it out to a file.
        try:
            with open("./output/" + title +".json", 'w', encoding='utf-8') as json_file:
                json_file.write(json_formatted)

            print(f'{(video_num/num_videos)*100:.2f}% {title} {video_id}')
        except:
            print("file name invalid" + title)
            with open("fileWriteError.txt", 'a') as f:
                f.write(video_id + " " + title)

def main():
    #url  = "https://www.youtube.com/watch?v=GFKHOiufjkI&list=UUxyCzPY2pjAjrxoSYclpuLg"
    #videos = pafy.get_playlist2(url)
    with open("videos.txt", "r") as videos:
        video_ids = videos.readlines()
    video_num = 0
    num_videos = len(video_ids)
    formatter = JSONFormatter()
    threads = list()
    for video_id in video_ids:
        video_num+=1
        x = threading.Thread(target=thread_function, args=(video_id, video_num, num_videos,))
        threads.append(x)
        x.start()
    for index, thread in enumerate(threads):
        thread.join()
       
if __name__ == "__main__":
    main()
