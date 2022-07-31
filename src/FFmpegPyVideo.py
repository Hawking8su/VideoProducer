'''
Python + ffmpeg制作视频
case1: zoom in (x，y)
case2: move from point A to point B
'''

import os
from PIL import Image


def make_ffmpeg_cmd(in_file, out_file, vf_str):
    return "ffmpeg -y -i {0} -vf \"{2}\" -pix_fmt yuv420p -c:v libx264 {1}".format(in_file, out_file, vf_str)


def cmd_execute(cmd_str=""):
    print("Executing cmd: {}".format(cmd_str))
    with os.popen(cmd_str) as f:
        cmd_output = str.join("\n", f.readlines())

    if cmd_output is not None and len(cmd_output) !=0:
        print("cmd_output: {}".format(cmd_output))
        return False
    return True


# make zoompan filter
# input: image size (width, height), (x,y), z, time
# default: output size = input size, duration = 25fps * time, scale=-2:10*ih
def vf_zoom(image_size=(0, 0), z_point=(0, 0), z_effect='', time=0):
    # ffplay -i liuyifei_3.jpg -vf "scale=-2:10*ih,zoompan=x='(iw-iw/zoom)*(475/640)':y='(ih-ih/zoom)*(125/359)':z='zoom+0.010':d=25*4:s=640x359"

    return "scale=-2:10*ih,zoompan=x='(iw-iw/zoom)*({0}/{2})':y='(ih-ih/zoom)*({1}/{3})':z='{4}':d=25*{5}:s={2}x{3}".format(
        z_point[0],
        z_point[1],
        image_size[0],
        image_size[1],
        z_effect,
        time
    )


# todo
def vf_crop_pad(image_size=(0, 0), z_point=(0, 0), z_effect='', time=0):
    # ffplay -i zoomtest03-liuyifei.mp4 -vf "crop=iw/2:ih:iw/2*t/5:0,pad=w=1280:h=800:x='(ow-iw)/2':y='(oh-ih)/2"
    return None


# return true/false
def resize_image(in_img_path, out_img_path, out_size=(0, 0)):
    try:
        in_image = Image.open(in_img_path)
    except:
        print("Error! resize_image(): open image {}".format(in_img_path))
        return False

    if out_size is None:
        image_size_origin = in_image.size
        # make size even, otherwise error when specify video size
        out_size = (
            image_size_origin[0] + 1 if (image_size_origin[0] % 2 == 1) else image_size_origin[0],
            image_size_origin[1] + 1 if (image_size_origin[1] % 2 == 1) else image_size_origin[1]
        )
        print("resize_image(): auto-adjusted output size {}".format(out_size))
    else:
        # check if output size is even， if not adjust to even
        if (out_size[0] % 2 == 1) or (out_size[1] % 2 == 1):
            origin_out_size = out_size
            out_size = (
                origin_out_size[0] + 1 if (origin_out_size[0] % 2 == 1) else origin_out_size[0],
                origin_out_size[1] + 1 if (origin_out_size[1] % 2 == 1) else origin_out_size[1]
            )
            print("resize_image(): Invalid output size {}! auto-adjusted output size {}.".format(origin_out_size,
                                                                                                 out_size))
    # out_img = in_image.resize(out_size, Image.ANTIALIAS)
    out_img = in_image.resize(out_size, Image.Resampling.LANCZOS)
    out_img.save(out_img_path)
    return True


# zoom in, move from point A to point B
def vf_zoom_move(in_file="", out_file="", out_size=(0, 0), point_start=(0, 0), point_end=(0, 0), z_effect=1, time=0,
                 move_speed=1):
    scale_ratio = 10
    upscale = f"{out_size[0] * scale_ratio}x{out_size[1] * scale_ratio}"
    out_scale = f"{out_size[0]}x{out_size[1]}"
    frame_rate = 25 * time
    move_frame_rate = frame_rate / move_speed
    vf_str = f'''
        scale={upscale},
        zoompan=
            x='({point_start[0]}+(on/{move_frame_rate})*({point_end[0] - point_start[0]}))*{scale_ratio}*(1-1/zoom):
            y='({point_start[1]}+(on/{move_frame_rate})*({point_end[1] - point_start[1]}))*{scale_ratio}*(1-1/zoom)':
            z='{z_effect}':
            d={frame_rate}:
            s={out_scale}
    '''
    return "ffmpeg -y -i {0} -vf \"{2}\" -pix_fmt yuv420p -c:v libx264 {1}".format(in_file, out_file,vf_str.replace("\n", "").replace(" ",""))



# stop n seconds
def vf_stop_effect(in_file="", out_file="", time=0):
    return f"ffmpeg -y -framerate 25 -loop 1 -i {in_file} -c:v libx264 -t {time} -pix_fmt yuv420p {out_file}"


# stop extract last or begin frame
def vf_extract_frame(in_file="", out_file="", frame="last"):
    ffmpeg_cmd = None
    if frame == "last":
        ffmpeg_cmd = f"ffmpeg -y -sseof -0.1 -i {in_file} -q:v 2 -update 1 {out_file}"
    elif frame == "first":
        ffmpeg_cmd = f"ffmpeg -y -i {in_file} -vf \"select=eq(n\,0)\" -q:v 3 {out_file}"
    return ffmpeg_cmd


# concat videos
def vf_concat_videos(in_files=[], out_file=""):
    list_file = 'concat_videos.txt';
    with open(list_file, 'w') as fh:
        for filename in in_files:
            if isinstance(filename, str) and filename.endswith('.mp4'):
                print(filename)
                fh.write("file '{}'\n".format(filename))
    return "ffmpeg -f concat -safe 0 -y -i {} -c copy {}".format(list_file, out_file)


if __name__ == '__main__':
    # Example command: ffplay -i liuyifei_3.jpg -vf "scale=-2:10*ih,zoompan=x='(iw-iw/zoom)*(475/640)':y='(ih-ih/zoom)*(125/359)':z='zoom+0.010':d=25*4:s=640x359"
    out_videos = []
    os.chdir("/Users/liuzuhao/PycharmProjects/VideoProducer")
    # step0: get input image
    in_filename = "windows_people.jpg"
    in_filename_base = os.path.splitext(in_filename)[0]
    in_file = "./image/{}".format(in_filename)
    resized_image_file = "./out/{}_resize.jpg".format(in_filename_base)

    # step1: resize image
    # out_size = (640, 360)
    out_size = (1920, 1280)
    result = resize_image(in_file, resized_image_file, out_size)
    if result:
        print("Success! Resize output image file: {}".format(resized_image_file))
    else:
        print("Failure! Resize input image file: {}".format(in_file))
    # step2: move from point A to point B
    out_file2 = "./out/{}_move1.mp4".format(in_filename_base)
    point_a = (1489, 278)
    point_b = (467, 371)
    z_multi = 2.8
    time = 4
    move_speed = 1

    ff_cmd = vf_zoom_move(in_file=resized_image_file
                          , out_file=out_file2
                          , out_size=out_size
                          , point_start=point_a
                          , point_end=point_b
                          , z_effect=z_multi
                          , time=time
                          , move_speed=move_speed
                          )
    cmd_output = cmd_execute(ff_cmd)
    out_videos.append(out_file2)

    # step3: extract the last frame and make a video for n seconds
    in_file3 = out_file2
    out_file3 = "./out/{}_extract_frame.jpg".format(in_filename_base)
    ff_cmd = vf_extract_frame(in_file=in_file3, out_file=out_file3, frame="last")
    cmd_output = cmd_execute(ff_cmd)
    # make a video for n seconds
    out_file4 = "./out/{}_extract_frame.mp4".format(in_filename_base)
    time = 1
    ff_cmd = vf_stop_effect(in_file=out_file3, out_file=out_file4, time=time)
    cmd_output = cmd_execute(ff_cmd)
    out_videos.append(out_file4)
    # step4: move from point B to point C
    out_file5 = "./out/{}_move2.mp4".format(in_filename_base)
    point_a = (467, 371)
    point_b = (1274, 580)
    z_multi = 2.8
    time = 4
    move_speed = 1

    ff_cmd = vf_zoom_move(in_file=resized_image_file
                          , out_file=out_file5
                          , out_size=out_size
                          , point_start=point_a
                          , point_end=point_b
                          , z_effect=z_multi
                          , time=time
                          , move_speed=move_speed
                          )
    cmd_output = cmd_execute(ff_cmd)
    out_videos.append(out_file5)

    # step5: concat videos to final video
    out_file_final = "./out/{}_final.mp4".format(in_filename_base)
    ff_cmd = vf_concat_videos(in_files=out_videos, out_file=out_file_final)
    print(ff_cmd)
    cmd_output = cmd_execute(ff_cmd)
    print(cmd_output)
    # todo: remove middle video and image files
    # todo: edge handle -- done
    print("Done!")
