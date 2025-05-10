import io
import shutil
import struct
import wave

# Desclaimer. This code is ineffient but it does the job.

def makeWAV(name : str):
    starting_sample = 0
    starting_frames = None

    with wave.open("begin/{}.wav".format(name)) as f:
        starting_sample = f.getnframes() - 1

        if f.getframerate() != 22050:
            print( f.getframerate(), "!= 22050" )
            return
        if f.getnchannels() != 1:
            print( f.getnchannels(), "!= 1" )
            return
        if f.getsampwidth() != 2:
            print( f.getsampwidth(), "!= 2" )
            return
        if f.getcomptype() != 'NONE':
            print( f.getcomptype(), "!= None" )
            return

        starting_frames = f.readframes( f.getnframes() )

    if starting_sample <= 0:
        print( "begin/{}.wav".format(name), "not found!" )
        return

    ending_sample = starting_sample
    ending_frames = None

    try:
        with wave.open("loop/{}.wav".format(name)) as f:
            ending_sample = starting_sample + f.getnframes() - 1

            if f.getframerate() != 22050:
                print( f.getframerate(), "!= 22050" )
                return
            if f.getnchannels() != 1:
                print( f.getnchannels(), "!= 1" )
                return
            if f.getsampwidth() != 2:
                print( f.getsampwidth(), "!= 2" )
                return
            if f.getcomptype() != 'NONE':
                print( f.getcomptype(), "!= None" )
                return

            ending_frames = f.readframes( f.getnframes() )

    except FileNotFoundError:
        pass

    if ending_sample == starting_sample:
        shutil.copyfile("begin/{}.wav".format(name), "output/{}.wav".format(name))

        print("No loop track added for", "output/{}.wav".format(name))

        return

    with wave.open("output/{}.wav".format(name), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(22050)
        f.writeframes(starting_frames)
        f.writeframes(ending_frames)

    data = bytearray(
        struct.pack(
            "<bbbbIIIIIIIIIIIIIIII",
            ord('s'), ord('m'), ord('p'), ord('l'), 60,
            0, 0,
            45351,
            60,
            0, 0, 0,
            1,
            0,
            0, 0,
            starting_sample, ending_sample,
            0, 0) )

    with open("output/{}.wav".format(name), "r+b") as f:
        f.seek(4)

        size = struct.unpack('I', f.read(4))[0] + len(data)

        f.seek(4)
        f.write( struct.pack('I', size) )

        f.seek(0, io.SEEK_END)
        f.write(data)


    print( "Loop track added for", "output/{}.wav".format(name) )

for i in range(1, 25):
    makeWAV("{}".format(i))
