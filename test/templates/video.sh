#!/bin/bash

base="/var/www/html"

cd $base

ffmpeg -fflags nobuffer \
 -rtsp_transport tcp \
 -i 'rtsp://<username>:<password>@{{camip}}/cam/realmonitor?channel=1&subtype=0' \
 -vsync 0 \
 -copyts \
 -vcodec copy \
 -movflags frag_keyframe+empty_moov \
 -an \
 -hls_flags delete_segments+append_list \
 -f segment \
 -segment_list_flags live \
 -segment_time 1 \
 -segment_list_size 3 \
 -segment_format mpegts \
 -segment_list /var/www/html/stream_{{randomno}}.m3u8 \
 -segment_list_type m3u8 \
 -segment_list_entry_prefix http://{{ localhostip }}/segments_{{randomno}}/ \
 /var/www/html/segments_{{randomno}}/%d.ts
