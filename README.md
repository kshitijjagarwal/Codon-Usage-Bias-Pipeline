The whole pipeline can be divided into 3 sections mainly. Before running CODEML, running CODEML and after running CODEML(working with the output files).

BEFORE CODEML
Download the tree files and and filtered NT sequences from Orthomam. Don’t apply species related constraints. That will be taken care of in subsequent points.

Suppose we download 1000 files which correspond to 1000 genes. The maximum number of species possible could be 190 in orthomam data as of June 2024. Our next task is to make a dictionary matrix which has all the 190 species possible as Row titles and let those 1000 genes be column titles. The cells would say Y/N corresponding to whether the particular species is present in that gene or not.

To make this matrix, we’ll use the Trees as they are easier to process than the NT sequence file. This would be done in 2 steps-
a.) The trees downloaded from ORTHOMAM have branch length and bootstrap values which need to be removed. For that use the PYTHON script “simplify.py”.
-Here the path to the input folder must be changed to the Trees directory downloaded from ORTHOMAM.
-Output tree files will be saved in the same Trees directory.
-These simplified tree files (without branch length and bootstrap values) can be copied and saved in a new directory (say simplified_trees).
b.) Now we take input of these simplified trees (in this case 1000 trees) to form a dictionary. Use the python script “dict.py”
-Here, the input would be the path of the directory where simplified trees are present. (in our case- simplified_trees)
-The output sheet would be saved in this directory itself named as- species_presence_matrix.xlsx

Now we need to know the number of genes a species is present in.
-Use the python script “chart.py”
-Here, the input would be the same as the previous one, the path to simplified_trees directory. Here, basically it goes into this directory, finds the species_presence_matrix.xlsx file and reads it.
-The output would be file- 
-In this excel sheet there are 2 sheets. The first one gives the count of genes in which every 190 species is present in descending order and a plot corresponding to it.
-The second excel sheet gives a the same table as of species_presence_matrix.xlsx
But just in descending order.

After analyzing this matrix we can choose the species with whom we need to proceed.

Suppose we choose 5 species and want to know how many genes are there which contain all these 5 species. For that I made a calculator.
-Use the python script “calci.py” and run it in the terminal. It will ask for input where you need to provide species name exactly as it is separated by spaces to get the output as an integer value.
-Modify the script by changing the directory path to where species_presence_matrix.xlsx file is present.

Though the calculator part is not necessary and doesn’t affect the pipeline, it gives a rough estimate of the number of genes we are going to deal with.

This the final and most important step before running CODEML.
-Use the python script “mapping.py”
-After running the script in the terminal it takes input of the desired species name which needs to be entered as it is separated by spaces.
-What this script does is, it finds all the tree files where these desired species are present from the- species_presence_matrix.xlsx and maps it to the NT alignment sequences file.
-Then after finding out the NT alignment files which have all the desired species, it scrapes sequences of only those desired species and puts them into a new directory.
-Suppose we had 5 desired species and 200 genes having all of these 5 species, then the output would be 200 directories named by their gene name.
-And every 200 directory inside them will have a ms.fasta file having sequences of only these 5 species for that particular gene.
-The point of doing this is only for our convenience to put it into CODEML.
-Modify the script accordingly, directory_path: the path to directory where species_presence_matrix.xlsx is present, ortho_directory: the path to directory where NT alignment sequences are present downloaded from orthomam, output_directory: the directory where you need your scraped out sequences should be saved.



 RUNNING CODEML
To run CODEML we need 3 things
Tree file(the newick tree of those desired species)
Sequences fasta file
Codeml control file

Tree file and codeml control file will be the same for all the genes we are going to analyze, while sequences of the fasta file would be unique.

In the new directory where sub directories for each gene was created earlier, add the codeml control file and tree file. 

Modify the control file first by specifying the tree file path and save changes.

Now to run CODEML simultaneously for multiple genes, I used the parallel command of the terminal which needs to be installed if not already present.

After downloading the parallel (if it was not present earlier), open parallel.sh file provided by me and edit the last line which is- 
find $MAIN_DIR -mindepth 1 -maxdepth 1 -type d | parallel -j 5 --workdir '{}' codeml /Users/kagarwal/Desktop/9560/codeml.ctl # the format should be - codeml 'patht to control file'
Add the path to codeml control file
You modify the number of task runs parallely being processed by changing the number “-j 5” . Here 5 corresponds to 5 tasks being run parallely.

I suggest you run the CODEML with 5-10 genes initially to test whether the output is as desired or not.

The output would be, processed data files being created and getting saved in every gene's sub directory.

AFTER CODEML
The most important processed output file for us is- rst

It has codon sequences of all the internal as well as leaf nodes, which we need to study codon usage bias.

 To extract the the part of rst file which has node sequences, both internal and leaf(species), run the python script “extract.py”
-It takes into input the rst file
-Gives the extracted sequences in output as “extracted_content.txt”

The “extracted_content.txt” file is not aligned uniformly, so to align it similar to fasta format use the python script “list3.py”
-It takes input of newick tree file of desired species “tree.nwk” and “extracted_content.txt”
-The script basically reads the newick tree and finds out leaf nodes(species name) and also their count.
-Uses this to find the internal node numbers and change it to a fasta type format easy for us to process it further.
-The output file is “output_sequences.txt”

For all the 64 codons, we need a frequency matrix, which says how many times a codon is present in a node(internal as well as leaf).
-Use the python script “frequency.py”
-It take input “output_sequences.txt”
-Output file is saved as “codon_frequency.csv”

We funnel this frequency matrix for each amino acid now.
-We know which codons code for the specific amino acid
-So the previous matrix is broken into separate excel sheets for each amino acid.
-Python script “amino.py”
-Input “codon_frequency.csv”
-Output “amino_acid_codon_frequencies.xlsx”

Since entropy calculations deals with probabilities/ratios we process these per amino acid frequency matrix into a probability table.
-Python script “prob.py”
-Input  “amino_acid_codon_frequencies.xlsx”
-Output  “amino_acid_codon_probabilities.xlsx”

Now we find the entropy using the formula for Shannon entropy where the base of the logarithm is taken as the number of codons for every amino acid. That is,  the base will be dynamic.
-The output is single excel matrix which has entropy listed for all amino acids except Methionine and Tryptophan (since only one codon code them)
-Python script “entropy2.py”
-Input “amino_acid_codon_probabilities.xlsx”
-Output “gene.xlsx”

After calculating entropy, we are majorly concerned about del(entropy), to compare biases across data.
-First we need to find out the node relations to figure out the branches, all this information is present in the “rst” file.
-Use python script “extseq.py” which takes into input “rst” file to scrape out this relation and save it as output “relation.txt”
-Now use the python script “difference.py” which takes input “gene.xlsx” and “relation.txt” to find entropy differences of branches.
-Output file saved as “entropy_differences.xlsx”

Now comes the compilation step to make a single file, which has a separate sheet for each amino acid.
-The compiled sheet for each amino acid will tell us the entropy difference for all the genes we are analyzing.
-Use the python script “plot_matrix.py”
-It goes into all the gene directories and takes input of “entropy_differences.xlsx”
-The output file is saved as “combined_entropy_differences.xlsx”

This “combined_entropy_differences.xlsx” file is the bible for analysis of any codon usage bias and end product of this long pipeline. This file can be used in multiple ways to supply sufficient insights.

I used this file to plot histograms.
-Python script “histogram.py”

Note: 
The steps 1-9 should be followed one after the other as each successive script takes into input the output file produced by the previous script.
The 3rd section of the pipeline i.e. AFTER CODEML should be tried with one gene file initially to check whether it’s giving output or not from steps 1-9.
If desired output is given, steps 1-9 can be run for all the gene files, one by one using the python script “combinedrun.py”
This script should be present in the main directory where all gene files/sub-directories are present along with the scripts required for steps 1-9.
Don’t forget to change the main directory path in this script.
Also we need to provide the path of the tree file which is common for all the genes in the “list3.py” script.

Following this pipeline, anyone can re-trace each and every thing on how 
I proceeded and re-produce the outputs.


