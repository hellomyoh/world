#!/bin/sh
# cron
# */1 * * * * /home/techops/Venice/v1/utils/webpConverter.sh

webp_files=`find . -type f -name "*.webp" -exec ls {} \;`

for file in ${webp_files}
do
    echo "${file} file"
    dwebp ${file} -o ${file}.jpg
done