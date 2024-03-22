export WORKDIR=/public/home/jiazhan/workplace/2023-Gene_Prediction/daishoulu/script
export LOGDIR=/public/home/jiazhan/workplace/2023-Gene_Prediction/daishoulu/script/log
export REFDIR=/public/home/jiazhan/workplace/2023-Gene_Prediction/daishoulu/ref
export OUTPUT=/public/home/jiazhan/workplace/2023-Gene_Prediction/daishoulu/result
export GENOME_LIST=/public/home/jiazhan/workplace/2023-Gene_Prediction/daishoulu/script/rerun.txt

# author: daishoulu
# 本脚本实验室内部参考，路径不做修改。
# 特别注意参数 -Xmx100G ，增加虚拟机的内存，否则会报内存溢出错误。

for genomes in $(cat ${GENOME_LIST})
do
    genome=$(echo ${genomes} | awk '{print substr($0, 1, 13)}')
    outputdir=${OUTPUT}/${genome}
    mkdir -p ${outputdir}
    cd ${outputdir}
    bsub -J ${genome} -n 20 -R "span[hosts=1] rusage[mem=110GB]" -o ${LOGDIR}/${genome}.%J.out -e ${LOGDIR}/${genome}.%J.err -q smp \
    "
        java -Xmx100G -jar /public/home/jiazhan/softwares/GeMoMa-1.9/GeMoMa-1.9.jar CLI GeMoMaPipeline \
            threads=20 \
            outdir=${outputdir} \
            GeMoMa.Score=ReAlign AnnotationFinalizer.r=NO p=false o=true tblastn=false \
            g=${REFDIR}/GCF_002263795.2_ARS-UCD1.3_genomic.fna.gz \
            a=${REFDIR}/GCF_002263795.2_ARS-UCD1.3_genomic.gff.gz \
            t=${REFDIR}/${genomes}.fna.gz

        mv ${outputdir}/final_annotation.gff ${outputdir}/${genome}.gff
    "
done
