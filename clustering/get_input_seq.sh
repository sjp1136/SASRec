in_file="data/Steam2.txt"
reviews="data/steam_reviews.json"
out_dir="data/user_seqs/"

rm $out_dir*

while read -r line; do
    read -ra line_arr <<<"$line"
    sed "${line_arr[2]}q;d" $reviews >> "${out_dir}user_${line_arr[0]}_input_seq.txt"
#    echo -e "\n" >> "${out_dir}user_${line_arr[0]}_input_seq.txt"
done < "$in_file"