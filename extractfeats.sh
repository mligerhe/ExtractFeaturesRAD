for feats in imagenet radimagenet vit swint
do
	echo "Running target: ${target}"
	python ${feats}.py /nfs/rnas/mligero/Github/GBM/data/brain_slice/T1/* --outdir /nfs/rnas/mligero/Github/FeatureExtraction_RAD/${feats}
done
