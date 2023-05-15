def __mstime_to_str(t: int) -> str:
    ms = t % 1000
    seconds = t//1000
    min = t//(1000*60)
    hour = t//(1000*60*60)
    seconds = seconds - min*60
    min = min - hour*60
    return "{:02d}:{:02d}:{:02d},{:03d}".format(hour, min, seconds, ms)

def lyrics_to_srt(input, output):

    import UnityPy

    count = 0
    last_lyric = 0
    with open(output, "w", encoding="utf-8") as f:
        for _, v in UnityPy.load(input).container.items():
            if v.type.name == "TextAsset":
                for line in bytes(v.read().script).decode("utf-8").splitlines():
                    content = line.strip().split(",")
                    if not content[0].isnumeric(): continue

                    lyric = "".join(content[1:])
                    lyric = lyric.strip()

                    if lyric:
                        count +=1
                        if count==1:
                            print(f"{count}", file=f)
                            print("{} -->".format(__mstime_to_str(int(content[0]))), file=f, end=" ")
                        else:
                            print("{}".format(__mstime_to_str(int(content[0])-1)), file=f)
                            print(last_lyric, file=f, end="\n\n")
                            print(f"{count}", file=f)
                            print("{} -->".format(__mstime_to_str(int(content[0]))), file=f, end=" ")

                        last_lyric = lyric

        print("{}".format(__mstime_to_str(int(content[0]))), file=f)
        print(last_lyric, file=f)