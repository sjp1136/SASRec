in_file="data/first_user_in_mapping_lines.txt"
reviews="data/steam_reviews.json"
out_dir="data/user_seqs/"

input_lines="405778 295770 2970274 6835251"
for line in $input_lines
do
    sed "${line}q;d" $reviews >> "${out_dir}user_221228_input_seq.txt"
done
#    echo -e "\n" >> "${out_dir}user_${line_arr[0]}_input_seq.txt"
