for feats in imagenet radimagenet vit swint
do
	echo "Running target: ${target}"
	python ${feats}.py /input/path/* --outdir /output/path/${feats}
done
