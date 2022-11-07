# Summarization
This guideline concerns the analysis of some text summary models using to improve digital reading of scientific papers. Three language models for the abstractive summarization approach have been selected and tested, with the aim of choosing the one that best summarises the content of each section of the paper, i.e. that is ables to extract the essential information and render the general sense of the source text coherently, generating new data correctly from the original text. 
## Data 
The selected corpus consists of 130 Open Access english scientific papers related to the fields of communication and education from the Spanish Journal "Comunicar: Scientific Journal of Media Education" [https://doi.org/10.3916/comunicar]. All the articles follow the IMRaD structure and are downloadable in xml format directly from the journal website. This journal was selected according to its active indexations 2022: it is a representative of national journals well positioned in the quartile (Q1) among scientific journals in the Social Sciences: Communication, Education and Cultural Studies. 
## Language Model for summary generation
Three language models, based on the abstractive summarization approach, have been analysed in the study: BART, PEGASUS and T5. 
## Summary human evaluation
For the evaluation of the extracted summaries, three levels of text quality measurement were established based on:
1. Content:
	- The content of the summary is relevant and coherent 
	- The summary is complete, the main ideas have been selected 
2. Spelling and Morphological correctness:
	- The spelling is correct
	- The morphosyntactic is correct
	- The punctuation is appropriate
 	 
3. Vocabulary and Style:
	- The summary is not identical to the original text, it rather introduces new data (sentences)
	- The length of the summary is suitable 

Based on these considerations, the human evaluations have been conducted using five ranking levels according to the Mean Opinion Score (MOS) scale:
1) Bad 
2) Poor
3) Fair
4) Good
5) Excellent
## Summary automatic evaluation
ROUGE method
## Interface 
https://obtic.sorbonne-universite.fr/summarizer/
