# -*- coding: utf-8 -*-
"""Assemble draft/*.md into 1bit-llm-survey.tex + generate references.bib + table .tex."""
import csv, re, os
os.chdir(r"c:\python experiments\survy papers\1 bit")
META = "scripts/pdf-metadata.tsv"  # <tab>-sep: local_file, arXiv-id-or-venue, title  (extracted once via pdftotext)

inv = {r['id']: r for r in csv.DictReader(open('data/inventory.csv', encoding='utf-8'))}
refs = {}
for line in open(META, encoding='utf-8', errors='replace'):
    p = line.rstrip('\n').split('\t')
    if len(p) >= 3:
        refs[p[0]] = (p[1].strip(), p[2].strip())

ARXIV_FIX = {
 '2024_Malinovskii_pv-tuning-beyond-ste.pdf': '2405.14852',
 '2024_Sundaram_llavaolmobitnet1b-ternary-llm-multimodal.pdf': '2408.13402',
 '2025_extra-rmsnorm-finetuning-to-1.58-bits.pdf': '2505.08823',
 '2025_Wang_bitnet-1bit-pretraining-JMLR.pdf': '',
}
TITLE_FIX = {
 '2024_Dong_stbllm-breaking-1bit-barrier-structural-binarization.pdf': 'STBLLM: Breaking the 1-Bit Barrier with Structured Binary LLMs',
 '2024_Tang_bi-mamba-1bit-state-space-models.pdf': 'Bi-Mamba: Towards Accurate 1-Bit State Space Models',
 '2025_Wang_bitnet-1bit-pretraining-JMLR.pdf': 'BitNet: 1-bit Pre-training for Large Language Models',
 '2025_addition-is-almost-all-you-need-double-binary-factorization.pdf': 'Addition is almost all you need: Compressing large language models with double binary factorization',
 '2025_bitnet-distillation.pdf': 'BitNet Distillation',
 '2025_multi-boolean-architectures-efficient-llms.pdf': 'Highly Efficient and Effective LLMs with Multi-Boolean Architectures',
 '2025_progressive-binarization-semi-structured-pruning-llm.pdf': 'Progressive Binarization with Semi-Structured Pruning for LLMs',
 '2025_tenet-sparsity-aware-lut-ternary-llm-edge.pdf': 'TENET: An Efficient Sparsity-Aware LUT-Centric Architecture for Ternary LLM Inference on Edge',
 '2026_NativeTernary-self-delimiting-binary-encoding-ternary-weights.pdf': 'NativeTernary: A Self-Delimiting Binary Encoding for Ternary Neural Network Weights',
 '2026_Litespark-simd-ternary-1.58bit-cpu.pdf': 'Litespark Inference for CPUs: Ultra-Fast SIMD Framework for Ternary (1.58-bit) Language Models',
 '2026_TOM-ternary-rom-accelerator-llm-edge.pdf': 'TOM: A Ternary Read-only Memory Accelerator for LLM-powered Edge Intelligence',
 '2026_hgf-hybrid-gated-flow-stabilizing-1.58bit-llms.pdf': 'Hybrid Gated Flow (HGF): Stabilizing 1.58-bit LLMs via Selective Low-Rank Correction',
 '2024_resilient-efficient-llms-efficiency-robustness.pdf': 'Towards Resilient and Efficient LLMs: A Comparative Study of Efficiency, Performance, and Adversarial Robustness',
 '2024_BEExformer-binarized-transformer-early-exits.pdf': 'BEExformer: A Fast Inferencing Binarized Transformer with Early Exits',
 '2022_Qin_bibert.pdf': 'BiBERT: Accurate Fully Binarized BERT',
 '2023_Yuan_pb-llm-partially-binarized.pdf': 'PB-LLM: Partially Binarized Large Language Models',
 '2024_Li_arb-llm-alternating-refined-binarization.pdf': 'ARB-LLM: Alternating Refined Binarizations for Large Language Models',
 '2025_Huang_Tequila-trapping-free-ternary-quantization.pdf': 'Tequila: Trapping-free Ternary Quantization for Large Language Models',
 '2025_PT2-LLM-post-training-ternarization.pdf': 'PT2-LLM: Post-Training Ternarization for Large Language Models',
 '2025_Tabesh_CAGE-curvature-aware-gradient-estimation.pdf': 'CAGE: Curvature-Aware Gradient Estimation for Accurate Quantization-Aware Training',
 '2026_nanoquant-sub-1bit-quantization-llms.pdf': 'NanoQuant: Efficient Sub-1-Bit Quantization of Large Language Models',
 '2025_challenging-gpu-dominance-cpu-on-device-llm.pdf': 'Challenging GPU Dominance: When CPUs Outperform for On-Device LLM Inference',
 '2026_EdgeRazor-mixed-precision-qad-lightweight-llm.pdf': 'EdgeRazor: A Lightweight Framework for LLMs via Mixed-Precision Quantization-Aware Distillation',
 '2025_iFairy-2bit-complex-llm-pm1-pmi.pdf': 'iFairy: the First 2-bit Complex LLM with All Parameters in $\\pm 1, \\pm i$',
 '2025_Fairy2i-complex-llm-from-real-llm.pdf': 'Fairy2i: Training Complex LLMs from Real LLMs',
}
VJ = {'JMLR': 'Journal of Machine Learning Research', 'Neural-Networks': 'Neural Networks',
      'TMLR': 'Transactions on Machine Learning Research',
      'IEEE-TPAMI': 'IEEE Transactions on Pattern Analysis and Machine Intelligence',
      'IEEE-RAL': 'IEEE Robotics and Automation Letters',
      'IEEE-TSUSC': 'IEEE Transactions on Sustainable Computing'}
VC = {'NeurIPS': 'Advances in Neural Information Processing Systems (NeurIPS)',
      'ICLR': 'International Conference on Learning Representations (ICLR)',
      'ICML': 'International Conference on Machine Learning (ICML)',
      'ACL': 'Annual Meeting of the Association for Computational Linguistics (ACL)',
      'Interspeech': 'Interspeech', 'COLM': 'Conference on Language Modeling (COLM)',
      'MLSys': 'Proceedings of Machine Learning and Systems (MLSys)',
      'ACML': 'Asian Conference on Machine Learning (ACML)',
      'EuroSys': 'European Conference on Computer Systems (EuroSys)',
      'DATE': 'Design, Automation and Test in Europe (DATE)',
      'ASP-DAC': 'Asia and South Pacific Design Automation Conference (ASP-DAC)',
      'CVPRW': 'IEEE/CVF CVPR Workshops', 'MobiSys': 'ACM MobiSys',
      'ECAI': 'European Conference on Artificial Intelligence (ECAI)'}

# Full author lists confirmed against the venue's own record (rather than the
# "first-author and others" placeholder every other entry still carries pending the
# camera-ready full-author pass), keyed by inventory id.
AUTHOR_FIX = {
 'Bengio2013-STE': 'Yoshua Bengio and Nicholas Léonard and Aaron Courville',
 'Courbariaux2015-BinaryConnect': 'Matthieu Courbariaux and Yoshua Bengio and Jean-Pierre David',
 'Rastegari2016-XNORNet': 'Mohammad Rastegari and Vicente Ordonez and Joseph Redmon and Ali Farhadi',
 'Bai2021-BinaryBERT': 'Haoli Bai and Wei Zhang and Lu Hou and Lifeng Shang and Jing Jin and '
                        'Xin Jiang and Qun Liu and Michael Lyu and Irwin King',
 'Qin2022-BiBERT': 'Haotong Qin and Yifu Ding and Mingyuan Zhang and Qinghua Yan and '
                    'Aishan Liu and Qingqing Dang and Ziwei Liu and Xianglong Liu',
 'Kim2023-TSLD': 'Minsoo Kim and Sihwa Lee and Janghwan Lee and Sukjin Hong and '
                  'Du-Seong Chang and Wonyong Sung and Jungwook Choi',
 'Wang2023-BitNet': 'Hongyu Wang and Shuming Ma and Li Dong and Shaohan Huang and '
                     'Huaijie Wang and Lingxiao Ma and Fan Yang and Ruiping Wang and Yi Wu and Furu Wei',
 'Shang2023-PBLLM': 'Yuzhang Shang and Zhihang Yuan and Qiang Wu and Zhen Dong',
 'Ansar2024-BEExformer': 'Wazib Ansar and Saptarsi Goswami and Amlan Chakrabarti',
 'Chen2024-DBLLM': 'Hong Chen and Chengtao Lv and Liang Ding and Haotong Qin and Xiabin Zhou and '
                    'Yifu Ding and Xuebo Liu and Min Zhang and Jinyang Guo and Xianglong Liu and Dacheng Tao',
 'Chen2024-EfficientQAT': 'Mengzhao Chen and Wenqi Shao and Peng Xu and Jiahao Wang and '
                           'Peng Gao and Kaipeng Zhang and Ping Luo',
 'Daliri2024-Theory1bit': 'Majid Daliri and Zhao Song and Chiwun Yang',
 'Dong2024-STBLLM': 'Peijie Dong and Lujun Li and Yuedong Zhong and Dayou Du and Ruibo Fan and '
                     'Yuhan Chen and Zhenheng Tang and Qiang Wang and Wei Xue and Yike Guo and Xiaowen Chu',
 'Du2024-BitDistiller': 'Dayou Du and Yijia Zhang and Shijie Cao and Jiaqi Guo and '
                         'Ting Cao and Xiaowen Chu and Ningyi Xu',
 'Das2024-GenBFA': 'Sanjay Das and Swastik Bhattacharya and Souvik Kundu and Shamik Kundu and '
                    'Anand Menon and Arnab Raha and Kanad Basu',
 'Gong2024-SurveyLowbit': 'Ruihao Gong and Yifu Ding and Zining Wang and Chengtao Lv and Xingyu Zheng and '
                           'Jinyang Du and Jinyang Guo and Xianglong Liu and Haotong Qin and Michele Magno and '
                           'Yang Yong and Shiqiao Gu and Dahua Lin',
 'Huang2024-BiLLM': 'Wei Huang and Yangdong Liu and Haotong Qin and Ying Li and Shiming Zhang and '
                     'Xianglong Liu and Michele Magno and Xiaojuan Qi',
 'Jo2024-BinaryMoS': 'Dongwon Jo and Taesu Kim and Yulhwa Kim and Jae-Joon Kim',
 'Kaushal2024-Spectra': 'Ayush Kaushal and Tejas Vaidhya and Arnab Kumar Mondal and '
                         'Tejas Pandey and Aaryan Bhagat and Irina Rish',
 'Zhao2024-DQT': 'Kaiyan Zhao and Tsuguchika Tabaru and Kenichi Kobayashi and Takumi Honda and '
                  'Masafumi Yamazaki and Yoshimasa Tsuruoka',
 'Kumar2024-ScalingLawsPrecision': 'Tanishq Kumar and Zachary Ankner and Benjamin F. Spector and '
                                    'Blake Bordelon and Niklas Muennighoff and Mansheej Paul and '
                                    'Cengiz Pehlevan and Christopher Ré and Aditi Raghunathan',
 'Li2024-ARBLLM': 'Zhiteng Li and Xianglong Yan and Tianao Zhang and Haotong Qin and Dong Xie and '
                   'Jiang Tian and Zhongchao Shi and Linghe Kong and Yulun Zhang and Xiaokang Yang',
 'Ma2024-BitNetB158': 'Shuming Ma and Hongyu Wang and Lingxiao Ma and Lei Wang and Wenhui Wang and '
                       'Shaohan Huang and Li Dong and Ruiping Wang and Jilong Xue and Furu Wei',
 'Ma2024-FBILLM': 'Liqun Ma and Mingjie Sun and Zhiqiang Shen',
 'Malekar2024-MatmulOrNot': 'Jinendra Malekar and Mohammed E. Elbtity and Ramtin Zand',
 'Malinovskii2024-PVTuning': 'Vladimir Malinovskii and Denis Mazur and Ivan Ilin and Denis Kuznedelev and '
                              'Konstantin Burlachenko and Kai Yi and Dan Alistarh and Peter Richtarik',
 'Nielsen2024-Reloaded': 'Jacob Nielsen and Peter Schneider-Kamp',
 'Nielsen2024-WhenEnough': 'Jacob Nielsen and Lukas Galke and Peter Schneider-Kamp',
 'Ouyang2024-QiDScaling': 'Xu Ouyang and Tao Ge and Thomas Hartvigsen and Zhisong Zhang and '
                           'Haitao Mi and Dong Yu',
 'Sundaram2024-LLaVaOLMoBitnet': 'Jainaveen Sundaram and Ravi Iyer',
 'Tang2024-BiMamba': 'Shengkun Tang and Liqun Ma and Haonan Li and Mingjie Sun and Zhiqiang Shen',
 'Wang2024-1bitAIInfra': 'Jinheng Wang and Hansong Zhou and Ting Song and Shaoguang Mao and '
                          'Shuming Ma and Hongyu Wang and Yan Xia and Furu Wei',
 'Wang2024-BitNetA48': 'Hongyu Wang and Shuming Ma and Furu Wei',
 'Wang2024-QSparse': 'Hongyu Wang and Shuming Ma and Ruiping Wang and Furu Wei',
 'Xu2024-OneBit': 'Yuzhuang Xu and Xu Han and Zonghan Yang and Shuo Wang and Qingfu Zhu and '
                   'Zhiyuan Liu and Weidong Liu and Wanxiang Che',
 'Zhu2024-MatmulFree': 'Rui-Jie Zhu and Yu Zhang and Steven Abreu and Ethan Sifferman and Tyler Sheaves and '
                        'Yiqiao Wang and Dustin Richmond and Sumit Bam Shrestha and Peng Zhou and Jason K. Eshraghian',
 'Dehghankar2024-EfficientMatmul': 'Mohsen Dehghankar and Mahdi Erfanian and Abolfazl Asudeh',
 'Chen2024-TernaryEmbedding': 'Jiayi Chen and Chen Wu and Shaoqun Zhang and Nan Li and '
                               'Liangjie Zhang and Qi Zhang',
 'Fan2024-ResilientEfficient': 'Xiaojing Fan and Chunliang Tao',
 'Kawamura2025-BitTTS': 'Masaya Kawamura and Takuya Hasumi and Yuma Shirahata and Ryuichi Yamamoto',
 'Ye2025-DBellQuant': 'Zijian Ye and Wei Huang and Yifei Yu and Tianhe Ren and Zhongrui Wang and Xiaojuan Qi',
 'Hoang2025-OutputAlign1bit': 'Hoang Anh Dung and Cuong Pham and Cuong Nguyen and Trung Le and '
                               'Thanh-Toan Do and Jianfei Cai',
 'Huang2025-Tequila': 'Hong Huang and Decheng Wu and Rui Cen and Guanghua Yu and Zonghang Li and '
                       'Kai Liu and Jianchen Zhu and Peng Chen and Xue Liu and Dapeng Wu',
 'Vaidhya2025-Spectra11': 'Tejas Vaidhya and Ayush Kaushal and Vineet Jain and Francis Couture-Harpin and '
                           'Prashant Shishodia and Majid Behbahani and Yuriy Nevmyvaka and Irina Rish',
 'Ardakani2025-LLMPi': 'Mahsa Ardakani and Jinendra Malekar and Ramtin Zand',
 'Lee2025-LittleBit': 'Banseok Lee and Dongkyu Kim and Youngcheon You and Youngmin Kim',
 'Liu2025-SurveyBNNLLM': 'Liangdong Liu and Zhitong Zheng and Cong Wang and Tianhuang Su and Zhenyu Yang',
 'Ma2025-BitNet2B4T': 'Shuming Ma and Hongyu Wang and Shaohan Huang and Xingxing Zhang and '
                       'Ying Hu and Ting Song and Yan Xia and Furu Wei',
 'Wang2025-MoTE': 'Hongyu Wang and Jiayu Xu and Ruiping Wang and Yan Feng and Yitao Zhai and '
                   'Peng Pei and Xunliang Cai and Xilin Chen',
 'Nielsen2025-ContinualQAT': 'Jacob Nielsen and Peter Schneider-Kamp and Lukas Galke',
 'Yan2025-PT2LLM': 'Xianglong Yan and Chengzhu Bao and Zhiteng Li and Tianao Zhang and Kaicheng Yang and '
                    'Haotong Qin and Ruobing Xie and Xingwu Sun and Yulun Zhang',
 'Xiao2025-PTQTP': 'He Xiao and Runming Yang and Qingyao Yang and Wendong Xu and Zhen Li and '
                    'Yupeng Su and Zhengwu Liu and Hongxia Yang and Ngai Wong',
 'Liu2025-ParetoQ': 'Zechun Liu and Changsheng Zhao and Hanxian Huang and Sijia Chen and Jing Zhang and '
                     'Jiawei Zhao and Scott Roy and Lisa Jin and Yunyang Xiong and Yangyang Shi and Lin Xiao and '
                     'Yuandong Tian and Bilge Soran and Raghuraman Krishnamoorthi and Tijmen Blankevoort and Vikas Chandra',
 'Panferov2025-QuEST': 'Andrei Panferov and Jiale Chen and Soroush Tabesh and Roberto L. Castro and '
                        'Mahdi Nikdan and Dan Alistarh',
 'Oh2025-TSAR': 'Hyunwoo Oh and KyungIn Nam and Rajat Bhattacharjya and Hanning Chen and Tamoghno Das and '
                 'Sanggeon Yun and Suyeon Jang and Andrew Ding and Nikil Dutt and Mohsen Imani',
 'Tabesh2025-CAGE': 'Soroush Tabesh and Mher Safaryan and Andrei Panferov and Alexandra Volkova and Dan Alistarh',
 'Xu2025-TeLLMe': 'Ye Qiao and Zhiheng Chen and Yifan Zhang and Yian Wang and Sitao Huang',
 'Chen2025-TerEffic': 'Chenyang Yin and Zhenyu Bai and Pranav Venkatram and Shivam Aggarval and '
                       'Zhaoying Li and Tulika Mitra',
 'Tu2025-Rethink1bitOpt': 'Zhijun Tu and Jian Li and Yuanyuan Xi and Siqi Liu and Chuanjian Liu and '
                           'Hanting Chen and Jie Hu and Yunhe Wang',
 'Wang2025-BitNetJMLR': 'Hongyu Wang and Shuming Ma and Lingxiao Ma and Lei Wang and '
                         'Wenhui Wang and Li Dong and Shaohan Huang and Huaijie Wang and '
                         'Jilong Xue and Ruiping Wang and Yi Wu and Furu Wei',
 'Wang2025-BitNetCPP': 'Jinheng Wang and Hansong Zhou and Ting Song and Shijie Cao and Yan Xia and '
                        'Ting Cao and Jianyu Wei and Shuming Ma and Hongyu Wang and Furu Wei',
 'Wang2025-BitNetV2': 'Hongyu Wang and Shuming Ma and Furu Wei',
 'Wang2025-BitVLA': 'Hongyu Wang and Chuyan Xiong and Ruiping Wang and Xilin Chen',
 'Anon2025-BinaryWA-PTQ': 'Siqing Song and Chuang Wang and Ruiqi Wang and Yi Yang and Xu-Yao Zhang',
 'Anon2025-DoubleBinaryFactorization': 'Vladimír Boža and Vladimír Macko',
 'Wu2025-BitNetDistillation': 'Xun Wu and Shaohan Huang and Wenhui Wang and Ting Song and Li Dong and '
                               'Yan Xia and Furu Wei',
 'Zhang2025-BitROM': 'Wenlun Zhang and Xinyu Li and Shimpei Ando and Kentaro Yoshioka',
 'Gu2025-BTCLLM': 'Hao Gu and Lujun Li and Hao Wang and Lei Wang and Zheyu Wang and Bei Liu and '
                   'Jiacheng Liu and Qiyuan Zhu and Sirui Han and Yike Guo',
 'Anon2025-CPUvsGPU': 'Haolin Zhang and Jeff Huang',
 'Anon2025-CompressionScalingLaws': 'Elias Frantar and Utku Evci and Wonpyo Park and Neil Houlsby and Dan Alistarh',
 'Chen2025-HBLLM': 'Ningning Chen and Weicai Ye and Ying Jiang',
 'Anon2025-STE-ZerothOrder': 'Ningfeng Yang and Tor M. Aamodt',
 'Chen2025-LoTAQAF': 'Junyu Chen and Junzhuo Li and Zhen Peng and Wenjie Wang and Yuxiang Ren and '
                      'Long Shi and Xuming Hu',
 'Hao2025-LowPrecTrainingSurvey': 'Zhiwei Hao and Jianyuan Guo and Li Shen and Yong Luo and Han Hu and '
                                   'Guoxia Wang and Dianhai Yu and Yonggang Wen and Dacheng Tao',
 'Anon2025-MultiBoolean': 'Ba-Hien Tran and Van Minh Nguyen',
 'Malekar2025-PIMLLM': 'Jinendra Malekar and Peyton Chandarana and Md Hasibul Amin and '
                        'Mohammed E. Elbtity and Ramtin Zand',
 'Anon2025-ProgBinPruning': 'Xianglong Yan and Tianao Zhang and Zhiteng Li and Haotong Qin and Yulun Zhang',
 'Zhao2025-PTQ161': 'Jiaqi Zhao and Miao Zhang and Ming Wang and Yuzhang Shang and Kaihao Zhang and '
                     'Weili Guan and Yaowei Wang and Min Zhang',
 'Xia2025-SDQLLM': 'Junhao Xia and Ming Zhao and Limin Xiao and Xiujun Zhang',
 'Anon2025-TENET': 'Zhirui Huang and Rui Ma and Shijie Cao and Ran Shu and Ian Wang and Ting Cao and '
                    'Chixiao Chen and Yongqiang Xiong',
 'Anon2025-VLMTernarization': 'Ben Crulis and Cyril De Runz and Barthelemy Serres and Gilles Venturini',
 'Anon2025-OneBitASR': 'Zhaoqing Li and Haoning Xu and Zengrui Jin and Lingwei Meng and Tianzi Wang and '
                        'Huimeng Wang and Youjun Chen and Mingyu Cui and Shujie Hu and Xunying Liu',
 'Connor2025-UltraQuantisation': 'Richard Connor and Alan Dearle and Ben Claydon',
 'Huang2026-Sherry': 'Hong Huang and Decheng Wu and Qiangqiang Hu and Guanghua Yu and Jinhai Yang and '
                      'Jianchen Zhu and Xue Liu and Dapeng Wu',
 'Li2026-BitNetTextEmbeddings': 'Zhen Li and Xin Huang and Liang Wang and Nan Yang and Ting Song and '
                                 'Yan Xia and Xun Wu and Shaohan Huang and Huishuai Zhang and Furu Wei and Dongyan Zhao',
 'Anon2026-Litespark': 'Nii Osae Osae Dade and Tony Morri and Sayandip Pal and Moinul Hossain Rahat and Rickston Pinto',
 'Anon2026-NativeTernary': 'Maharshi Savdhariya',
 'Song2026-LBLLM': 'Siqing Song and Chuang Wang and Yong Lang and Yi Yang and Xu-Yao Zhang',
 'Nargund2026-TernaryLM': 'Nisharg Nargund and Priyesh Shukla',
 'Zhang2026-SparseBitNet': 'Di Zhang and Xun Wu and Shaohan Huang and Yudong Wang and Hanyong Shao and '
                            'Yingbo Hao and Zewen Chi and Li Dong and Ting Song and Yan Xia and '
                            'Zhifang Sui and Furu Wei',
 'Zhao2026-TWLA': 'Zhixiong Zhao and Zukang Xu and Zhixuan Chen and Xing Hu and Zhe Jiang and Dawei Yang',
 'Zuo2026-FairyFuse': 'Fei Zuo and Xiaoyan Xi and Quanyi Zeng and Feiyu Wang and Ho Fai Leung',
 'Wang2026-CATQ': 'Shigeng Wang and Chao Li and Yangyuxuan Kang and Jiawei Fan and Anbang Yao',
 'Anon2026-EveryBitCounts': 'Sayak Chakrabarti and Toniann Pitassi and Josh Alman',
 'Anon2026-ExpressivePowerWQ': 'Shao-Qun Zhang',
 'Wang2026-HESTIA': 'Guoan Wang and Feiyu Wang and Zongwei Lv and Yikun Zong and Tong Yang',
 'Anon2026-HGF': 'David Alejandro Trejo Pizzo',
 'Chong2026-NanoQuant': 'Hyochan Chong and Dongkyu Kim and Changdong Kim and Minseop Choi',
 'You2026-RaBiT': 'Youngcheon You and Banseok Lee and Minseop Choi and Seonyoung Kim and Hyochan Chong and '
                   'Changdong Kim and Youngmin Kim and Dongkyu Kim',
 'Zagitov2026-HARP': 'Artur Zagitov and Gleb Molodtsov and Aleksandr Beznosikov',
 'Pavlov2026-InfluenceRotations': 'Gorgi Pavlov',
 'Zhang2026-pQuant': 'Wenzheng Zhang and Bingzheng Liu and Yang Hu and Xiaoying Bai and '
                      'Wentao Zhang and Bin Cui',
 'Wang2026-LCQAT': 'Haoyu Wang and Xingyu Yu and Haiyan Zhao and Fengxiang Wang and Xu Han',
 'Alimaskina2026-ExtremeReasoning': 'Ekaterina Alimaskina and Darya Rudas and Denis Shveykin and '
                                     'Gleb Molodtsov and Pavel Vasiliev and Aleksandr Beznosikov',
 'Zhao2026-BWLA': 'Zhixiong Zhao and Zukang Xu and Dawei Yang',
 'Xu2026-FittingNotEnough': 'Yuzhuang Xu and Xu Han and Yuxuan Li and Pengzhan Li and Wanxiang Che',
 'Wang2025-Fairy2i': 'Feiyu Wang and Xinyu Tan and Bokai Huang and Yihao Zhang and Guoan Wang and '
                      'Peizhuang Cong and Tong Yang',
 'Maskey2026-1BitWonder': 'Sohir Maskey and Constantin Eichenberg and Johannes Messner and Douglas Orr',
 'Li2025-ICQuant': 'Xinlin Li and Osama Hanna and Christina Fragouli and Suhas Diggavi',
 'Wang2025-TZLLM': 'Xunjie Wang and Jiacheng Shi and Zihan Zhao and Yang Yu and Zhichao Hua and Jinyu Gu',
 'Shan2025-Platinum': 'Haoxuan Shan and Cong Guo and Chiyue Wei and Feng Cheng and Junyao Zhang and '
                       'Hai Li and Yiran Chen',
 'Li2025-VecLUT': 'Xiangyu Li and Chengyu Yin and Weijun Wang and Jianyu Wei and Ting Cao and Yunxin Liu',
 'Guan2026-TOM': 'Hongyi Guan and Yijia Zhang and Wenqiang Wang and Yizhao Gao and Shijie Cao and '
                  'Chen Zhang and Ningyi Xu',
 'Qiao2025-TeLLMev2': 'Ye Qiao and Zhiheng Chen and Yifan Zhang and Yian Wang and Sitao Huang',
 'Jorgensen2025-ResourceEfficientLMs': 'Tollef Emil Jørgensen',
 'Aman2025-BitMar': 'Euhid Aman and Esteban Carlin and Hsing-Kuo Pao and Giovanni Beltrame and '
                     'Ghaluh Indah Permata Sari and Yie-Tarng Chen',
 'Chen2025-R2Q': 'Jiayi Chen and Jieqi Shi and Jing Huo and Chen Wu',
 'Zhang2026-EdgeRazor': 'Shu-Hao Zhang and Le-Tong Huang and Xiang-Sheng Deng and Xin-Yi Zou and Chen Wu and '
                         'Nan Li and Shao-Qun Zhang and Zhi-Hua Zhou',
 'Dehghankar2026-RSRcore': 'Mohsen Dehghankar and Abolfazl Asudeh',
 'Grainge2025-TeTRAVPR': 'Oliver Grainge and Michael Milford and Indu Bodala and '
                          'Sarvapali D. Ramchurn and Shoaib Ehsan',
 'Wang2025-iFairy': 'Feiyu Wang and Guoan Wang and Yihao Zhang and Shengfan Wang and Weitao Li and '
                     'Bokai Huang and Shimao Chen and Zihan Jiang and Rui Xu and Tong Yang',
 'Ganesaraja2026-TernaryMamba': 'Ramprasath Ganesaraja and Sahil Dilip Panse and Swathika N',
 'Zhang2025-TernaryCLIP': 'Shu-Hao Zhang and Wei-Cheng Tang and Chen Wu and Peng Hu and Nan Li and '
                           'Liang-Jie Zhang and Qi Zhang and Shao-Qun Zhang',
 'Steinmetz2025-ExtraRMSNorm': 'Cody Steinmetz and Gavin Childress and Aaron Herbst and Gavin Jones and '
                                'Jasdeep Singh and Eli Vang and Keagan Weinstock',
 'Ortega2024-PIMAI': 'Cristobal Ortega and Yann Falevoz and Renaud Ayrignac',
 'Liu2023-BinTernNLG': 'Zechun Liu and Barlas Oğuz and Yangyang Shi',
 'Wei2024-TMAC': 'Jianyu Wei and Shijie Cao and Ting Cao and Lingxiao Ma and Lei Wang and '
                  'Yanyong Zhang and Mao Yang',
 'Ji2024-BMTBAT': 'Yuhao Ji and Chao Fang and Shaobo Ma and Haikuo Shao and Zhongfeng Wang',
 'Xu2024-CRVQ': 'Yuzhuang Xu and Shiyu Ji and Qingfu Zhu and Wanxiang Che',
 'Edalati2024-OAC': 'Ali Edalati and Alireza Ghaffari and Mahsa Ghazvini Nejad and Lu Hou and '
                     'Boxing Chen and Masoud Asgharian and Vahid Partovi Nia',
 'Malhotra2025-ReTern': 'Akul Malhotra and Sumeet Kumar Gupta',
 'Xiao2025-LieQ': 'He Xiao and Qingyao Yang and Dirui Xie and Wendong Xu and Zunhai Su and '
                   'Runming Yang and Haobo Liu and Wenyong Zhou and Zhengwu Liu and Ngai Wong',
 'Georganas2025-UltraLowBitKernels': 'Evangelos Georganas and Dhiraj Kalamkar and Alexander Heinecke and Pradeep Dubey',
 'Qi2025-DeltaLLM': 'Jiawen Qi and Chang Gao and Zhaochun Ren and Qinyu Chen',
 'Zhang2025-PDSwap': 'Yifan Zhang and Zhiheng Chen and Ye Qiao and Sitao Huang',
 'Sajid2026-BitRL': 'Md. Ashiq Ul Islam Sajid and Mohammad Sakib Mahmood and Md. Tareq Hasan and '
                     'Md Abdur Rahim and Rafat Ara and Md. Arafat Hossain',
 'Geens2026-LUTAccelDesign': 'Robin Geens and Joran Heldens and Joren Dumoulin and Marian Verhelst',
 'Lin2026-VitaLLM': 'Zi-Wei Lin and Tian-Sheuan Chang',
 'Kang2026-BitTP': 'Mincheol Kang and Hyunjin Lim and Bomin Kang and Daehee Park',
 'Abdalla2026-SAGEPTQ': 'Rayyan Abdalla and Amir Hussein and Min Wu and Dinesh Manocha',
}
# Extra bibtex fields for entries whose identifier the arXiv-regex path above cannot
# supply (a JMLR-only record with no matching preprint id), sourced from the venue's own
# bibtex record rather than guessed.
EXTRA_FIELDS = {
 'Wang2025-BitNetJMLR': [('volume', '{26}'), ('number', '{125}'), ('pages', '{1--29}'),
                          ('url', '{http://jmlr.org/papers/v26/24-2050.html}')],
}

def clean_title(t):
    t = re.sub(r'\s+', ' ', t).strip().strip('.')
    if t.isupper() and len(t) > 8:
        t = t.title().replace('Llm', 'LLM').replace('Llms', 'LLMs').replace('Bert', 'BERT')
    return t

def bib_entry(rid):
    r = inv[rid]; lf = r['local_file']
    arx, rawt = refs.get(lf, ('', ''))
    if lf in ARXIV_FIX:
        arx = ('arXiv:' + ARXIV_FIX[lf]) if ARXIV_FIX[lf] else ''
    m = re.search(r'(\d{4}\.\d{4,5})', arx or '')
    aid = m.group(1) if m else ''
    title = TITLE_FIX.get(lf) or clean_title(rawt) or rid
    yr = re.sub(r'\D', '', r['year'])[:4] or r['year']
    fa = r['first_author']
    author = AUTHOR_FIX.get(rid) or ((fa + ' and others') if fa and fa not in ('NR', 'Anon', '') else '{Author list --- fill from PDF}')
    ven = r['venue']
    fld = [('title', '{%s}' % title), ('author', '{%s}' % author), ('year', '{%s}' % yr)]
    etype = 'misc'
    for k, j in VJ.items():
        if k in ven:
            etype = 'article'; fld.append(('journal', '{%s}' % j)); break
    else:
        for k, bt in VC.items():
            if k in ven:
                etype = 'inproceedings'; fld.append(('booktitle', '{%s}' % bt)); break
    if etype == 'misc':
        if aid:
            fld += [('eprint', '{%s}' % aid), ('archivePrefix', '{arXiv}'),
                    ('primaryClass', '{cs.LG}'), ('note', '{arXiv:%s}' % aid)]
        else:
            fld.append(('howpublished', '{%s}' % (ven or 'preprint')))
    elif aid:
        fld.append(('note', '{Also arXiv:%s}' % aid))
    # every arXiv record has a registered DataCite DOI of this exact form; add it and the
    # canonical abstract URL so the bibliography carries a resolvable identifier.
    if aid:
        fld.append(('doi', '{10.48550/arXiv.%s}' % aid))
        fld.append(('url', '{https://arxiv.org/abs/%s}' % aid))
    fld += EXTRA_FIELDS.get(rid, [])
    out = ['@%s{%s,' % (etype, rid)] + ['  %-14s = %s,' % kv for kv in fld]
    out[-1] = out[-1].rstrip(',')
    return '\n'.join(out + ['}'])

WEB = {
 'web-microsoftBitNet': '@misc{web-microsoftBitNet,\n  title  = {{bitnet.cpp: Official Inference Framework for 1-bit LLMs}},\n  author = {{Microsoft}},\n  year   = {2026},\n  howpublished = {\\url{https://github.com/microsoft/BitNet}},\n  note   = {accessed 2026-09-03}\n}',
 'web-falconEdge': '@misc{web-falconEdge,\n  title  = {{Falcon-Edge: Powerful, Universal, Fine-tunable 1.58bit Language Models}},\n  author = {{Falcon-LLM Team, TII}},\n  year   = {2025},\n  howpublished = {\\url{https://huggingface.co/blog/tiiuae/falcon-edge}},\n  note   = {accessed 2026-09-03}\n}',
 'web-bitnet2b4tCard': '@misc{web-bitnet2b4tCard,\n  title  = {{microsoft/bitnet-b1.58-2B-4T Model Card}},\n  author = {{Microsoft}},\n  year   = {2025},\n  howpublished = {\\url{https://huggingface.co/microsoft/bitnet-b1.58-2B-4T}},\n  note   = {accessed 2026-09-03}\n}',
 'web-bitnetIssue608': '@misc{web-bitnetIssue608,\n  title  = {{Current bitnet-b1.58-2B-4T checkpoints contain all-zero MLP weight tensors (model generates garbage), GitHub issue \\#608}},\n  author = {{grave0x}},\n  year   = {2026},\n  howpublished = {\\url{https://github.com/microsoft/BitNet/issues/608}},\n  note   = {opened 2026-08-11, accessed 2026-09-14}\n}',
}
WEB_YEAR = {'web-microsoftBitNet': 2026, 'web-falconEdge': 2025, 'web-bitnet2b4tCard': 2025,
            'web-bitnetIssue608': 2026}

def entry_year(rid):
    if rid in WEB_YEAR:
        return WEB_YEAR[rid]
    yr = re.sub(r'\D', '', inv[rid]['year'])[:4]
    return int(yr) if yr.isdigit() else 0

# Grouped by year, newest first, alphabetically by citation key within a year. This is
# purely for human navigation of the .bib file: unsrtnat numbers the printed bibliography
# by order of first citation in the text (Section-standing convention), not by .bib file
# order, so this re-sort changes nothing in the compiled paper.
with open('references.bib', 'w', encoding='utf-8') as f:
    f.write('%% Auto-generated, grouped by year (newest first; alphabetical by key within a\n'
            '%% year). This ordering is for human navigation only -- unsrtnat numbers the\n'
            '%% printed bibliography by first-citation order in the text, not by file order.\n'
            '%% Author fields are "first-author and others" pending a manual full-author pass\n'
            '%% for camera-ready. Every arXiv record carries its registered 10.48550/arXiv.*\n'
            '%% DOI and abstract URL; venue records also name the venue.\n\n')
    all_ids = sorted(list(inv) + list(WEB), key=lambda rid: (-entry_year(rid), rid))
    cur_year = None
    for rid in all_ids:
        yr = entry_year(rid)
        if yr != cur_year:
            cur_year = yr
            f.write('%%%% ---------- %s ----------\n\n' % (yr if yr else 'undated'))
        f.write((WEB[rid] if rid in WEB else bib_entry(rid)) + '\n\n')
print('references.bib:', len(inv) + len(WEB), 'entries')

# ---------- unicode normalisation ----------
UNI = {'\u2014': '---', '\u2013': '--', '\u2192': '$\\rightarrow$', '\u2248': '$\\approx$',
       '\u2264': '$\\le$', '\u2265': '$\\ge$', '\u00d7': '$\\times$', '\u00b1': '$\\pm$',
       '\u2026': '\\ldots{}', '\u00b7': '$\\cdot$', '\u00b0': '\\textdegree{}',
       '\u223c': '$\\sim$', '\u00a0': '~', '\u201c': '``', '\u201d': "''",
       '\u2018': '`', '\u2019': "'", '\u03ba': '$\\kappa$', '\u03bb': '$\\lambda$',
       '\u03b1': '$\\alpha$', '\u03b2': '$\\beta$', '\u03b3': '$\\gamma$', '\u03bc': '$\\mu$',
       '\u03c3': '$\\sigma$', '\u0394': '$\\Delta$', '\u221e': '$\\infty$',
       '\u00b2': '\\textsuperscript{2}', '\u00bd': '1/2', '\u2011': '-', '\u2212': '$-$'}
def uni(s):
    for a, b in UNI.items():
        s = s.replace(a, b)
    return s

# British -> American spelling safety net (whole words / stems that occur in the drafts)
_SPELL = [('behaviour', 'behavior'), ('Behaviour', 'Behavior'), ('neighbourhood', 'neighborhood'),
          ('neighbour', 'neighbor'), ('colour', 'color'), ('favour', 'favor'), ('licence', 'license'),
          ('artefact', 'artifact'), ('modelling', 'modeling'), ('centre', 'center'),
          ('analysed', 'analyzed'), ('analysing', 'analyzing'), ('catalogue', 'catalog'),
          ('programme', 'program'),
          ('optimisation', 'optimization'), ('optimise', 'optimize'), ('optimised', 'optimized'),
          ('quantisation', 'quantization'), ('quantise', 'quantize'), ('quantised', 'quantized'),
          ('normalisation', 'normalization'), ('normalise', 'normalize'), ('normalised', 'normalized'),
          ('organisation', 'organization'), ('organise', 'organize'), ('organised', 'organized'),
          ('formalised', 'formalized'), ('generalise', 'generalize'), ('sparsif', 'sparsif')]
# 'analyse' -> 'analyze' cannot be a plain substring rule like the others above: "analyse" is
# itself a substring of "analyses", which is the plural of the noun "analysis" (unchanged in
# American English) and must NOT be rewritten to "analyzes" (the American verb form). A
# negative lookahead skips exactly that case while still catching the bare verb "analyse".
_ANALYSE_VERB = re.compile(r'\banalyse(?!s\b)')
def spell(s):
    for a, b in _SPELL:
        if a != b:
            s = s.replace(a, b)
    s = _ANALYSE_VERB.sub('analyze', s)
    return s

# ---------- md -> tex ----------
CITE_MAP = {'_web/microsoft-BitNet': 'web-microsoftBitNet', '_web/falcon-edge': 'web-falconEdge',
            '_web/bitnet-b1.58-2B-4T': 'web-bitnet2b4tCard',
            'methodology': 'sec:method', 'sec:repro': 'sec:repro',
            'fig:taxonomy': 'fig:taxonomy', 'fig:efficiency': 'fig:efficiency',
            'fig:timeline': 'fig:timeline', 'fig:datapath': 'fig:datapath',
            'fig:roadmap': 'fig:roadmap', 'fig:growth': 'fig:growth',
            'fig:heatmap': 'fig:heatmap', 'fig:effbits': 'fig:effbits',
            'fig:controlledpairs': 'fig:controlledpairs', 'fig:ste': 'fig:ste',
            'fig:weightyear': 'fig:weightyear', 'fig:systemsvenn': 'fig:systemsvenn',
            'tab:classification': 'tab:classification', 'tab:results': 'tab:results',
            'tab:acc-primary': 'tab:acc-primary', 'tab:acc-controlled': 'tab:acc-controlled',
            'tab:quant-cost': 'tab:quant-cost', 'tab:efficiency': 'tab:efficiency',
            'tab:repro-audit': 'tab:repro-audit', 'tab:gsm8k': 'tab:gsm8k'}
KNOWN = set(inv) | set(WEB)

def convert_inline(s):
    codes = []
    s = re.sub(r'`([^`]+)`', lambda m: codes.append(m.group(1)) or '\x00C%d\x00' % (len(codes) - 1), s)
    # GGUF / llama.cpp quant-format and kernel identifiers -> monospace, handled like
    # inline code so underscores are escaped and they read as identifiers, not prose.
    s = re.sub(r'\b(I2_S|TL[12]|Q\d+_K_[SML]|Q\d+_K|Q\d+_[01])\b',
               lambda m: codes.append(m.group(1)) or '\x00C%d\x00' % (len(codes) - 1), s)
    maths = []
    s = re.sub(r'\$[^$\n]+\$', lambda m: maths.append(m.group(0)) or '\x00M%d\x00' % (len(maths) - 1), s)
    # markdown links [text](https://...) -> \href{url}{text}; protected as an opaque
    # token BEFORE the citation-bracket regex below (which would otherwise try to read
    # "[text]" as a citation key) and before the character-escaping loop (which would
    # otherwise mangle the backslash/braces of \href itself).
    links = []
    def _link(m):
        text, url = m.group(1), m.group(2)
        for a, b in [('\\', '\\textbackslash{}'), ('&', '\\&'), ('%', '\\%'), ('#', '\\#'),
                     ('_', '\\_'), ('{', '\\{'), ('}', '\\}'), ('$', '\\$'),
                     ('~', '\\textasciitilde{}'), ('^', '\\textasciicircum{}')]:
            text = text.replace(a, b)
        url_safe = url.replace('%', '\\%').replace('#', '\\#').replace('_', '\\_').replace('&', '\\&')
        links.append('\\href{%s}{%s}' % (url_safe, text))
        return '\x00U%d\x00' % (len(links) - 1)
    s = re.sub(r'\[([^\]\n]+)\]\((https?://[^\s)]+)\)', _link, s)
    cites = []
    def _cite(m):
        keys = re.findall(r'\[([A-Za-z0-9_.:/\-]+)\]', m.group(0))
        mp = []
        for k in keys:
            if k in CITE_MAP:
                v = CITE_MAP[k]
                mp.append('REF:' + v if v.startswith(('sec:', 'fig:', 'tab:')) else v)
            elif k in KNOWN:
                mp.append(k)
        if not mp:
            return m.group(0)
        refs_ = [x[4:] for x in mp if x.startswith('REF:')]
        cts = [x for x in mp if not x.startswith('REF:')]
        parts = []
        if cts:
            parts.append('\\cite{%s}' % ','.join(cts))
        for r in refs_:
            parts.append('\\ref{%s}' % r)   # prose already supplies the word "Section" / "Fig." / "Table"
        cites.append(' '.join(parts))
        return '\x00K%d\x00' % (len(cites) - 1)
    s = re.sub(r'(\[[A-Za-z0-9_.:/\-]+\](?:[,;]?\s*\[[A-Za-z0-9_.:/\-]+\])*)', _cite, s)
    for a, b in [('\\', '\\textbackslash{}'), ('&', '\\&'), ('%', '\\%'), ('#', '\\#'),
                 ('_', '\\_'), ('{', '\\{'), ('}', '\\}'), ('$', '\\$'),
                 ('~', '$\\sim$'), ('^', '\\textasciicircum{}')]:   # '~' means "approximately" in our prose
        s = s.replace(a, b)
    s = uni(s)
    s = spell(s)
    s = s.replace('<=', '$\\le$').replace('>=', '$\\ge$')
    s = re.sub(r'->', '$\\\\rightarrow$', s)
    # straight double quotes -> LaTeX quotes
    s = re.sub(r'"([^"\n]+)"', r"``\1''", s)
    # four-digit year ranges -> en dash
    s = re.sub(r'\b((?:19|20)\d\d)-((?:19|20)\d\d)\b', r'\1--\2', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', s)
    s = re.sub(r'(?<![\*\w])\*([^*\n]+?)\*(?!\*)', r'\\emph{\1}', s)
    for i, c in enumerate(codes):
        cc = (c.replace('\\', '\\textbackslash{}').replace('_', '\\_').replace('{', '\\{')
                .replace('}', '\\}').replace('%', '\\%').replace('&', '\\&').replace('#', '\\#')
                .replace('$', '\\$').replace('~', '\\textasciitilde{}').replace('^', '\\textasciicircum{}'))
        s = s.replace('\x00C%d\x00' % i, '\\texttt{%s}' % cc)
    for i, c in enumerate(maths):
        s = s.replace('\x00M%d\x00' % i, c)
    for i, c in enumerate(cites):
        s = s.replace('\x00K%d\x00' % i, c)
    for i, c in enumerate(links):
        s = s.replace('\x00U%d\x00' % i, c)
    return s

def convert_file(path, tag):
    lines = open(path, encoding='utf-8').read().split('\n')
    out, i, in_code, in_list = [], 0, False, None
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith('```'):
            out.append('\\end{verbatim}' if in_code else '\\begin{verbatim}')
            in_code = not in_code; i += 1; continue
        if in_code:
            out.append(ln); i += 1; continue
        st = ln.strip()
        if st.startswith('> '):
            i += 1; continue
        if not st:
            if in_list: out.append('\\end{%s}' % in_list); in_list = None
            out.append(''); i += 1; continue
        if st.startswith('|'):
            tbl = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                tbl.append(lines[i].strip()); i += 1
            # optional caption on a line after zero or more blank lines:
            #   "Table: {#tab:key} <text>"  -> a numbered \begin{table} float
            #   "Table*: <text>"            -> unnumbered \captionof* in a \begin{center}
            #   (none)                       -> the old unnumbered \begin{center} block
            cap = lbl = None
            star = False
            j = i
            while j < len(lines) and not lines[j].strip():
                j += 1
            mcap = re.match(r'^Table(\*?):\s*(.+)$', lines[j].strip()) if j < len(lines) else None
            if mcap:
                star = mcap.group(1) == '*'
                ctxt = mcap.group(2).strip()
                mlbl = re.match(r'^\{#(tab:[A-Za-z0-9_-]+)\}\s*(.+)$', ctxt)
                if mlbl:
                    lbl, ctxt = mlbl.group(1), mlbl.group(2).strip()
                cap = convert_inline(ctxt)
                i = j + 1
            is_dash_row = lambda r: re.match(r'^\|[\s:\-\|]+\|$', r)
            # the header's own separator row is always dropped; a SECOND dashes-only
            # row placed later in the table (by the .md author) is kept and rendered
            # as an explicit \midrule, e.g. to separate two groups of data rows.
            header_seen = False
            body = []
            for r in tbl:
                if is_dash_row(r):
                    if not header_seen:
                        header_seen = True  # this is the header/body separator; drop it
                    else:
                        body.append(r)  # a mid-table divider; keep as a marker
                    continue
                body.append(r)
            ncol = body[0].count('|') - 1
            cellrows = [[c.strip() for c in r.strip('|').split('|')] for r in body]
            maxw = [max((len(row[k]) for row in cellrows if k < len(row)), default=0)
                    for k in range(ncol)]
            # wide tables get wrapping columns (tabularx) so nothing overflows the text block;
            # narrow numeric tables keep their natural width.
            wide = sum(maxw) + 3 * ncol > 82 or any(w > 26 for w in maxw)
            if cap and not star:
                out.append('\\begin{table}[htbp]\\centering')
                out.append('\\caption{%s}' % cap)
                if lbl:
                    out.append('\\label{%s}' % lbl)
                out.append('\\footnotesize')
                close = '\\end{table}'
            else:
                out.append('\\begin{center}\\footnotesize')
                if cap and star:
                    out.append('\\captionof*{table}{\\footnotesize %s}\\par\\medskip' % cap)
                close = '\\end{center}'
            if wide:
                spec = ''.join('l' if w <= 10 else 'L' for w in maxw)
                if 'L' not in spec:
                    spec = 'L' * ncol
                out.append('\\begin{tabularx}{\\linewidth}{%s}\\toprule' % spec)
                endt = '\\bottomrule\\end{tabularx}'
            else:
                out.append('\\begin{tabular}{%s}\\toprule' % ('l' * ncol))
                endt = '\\bottomrule\\end{tabular}'
            for k, r in enumerate(body):
                if k > 0 and is_dash_row(r):
                    out.append('\\midrule')
                    continue
                cells = [convert_inline(c.strip()) for c in r.strip('|').split('|')]
                out.append(' & '.join(cells) + ' \\\\')
                if k == 0: out.append('\\midrule')
            out.append(endt + close)
            continue
        m = re.match(r'^(#{1,4})\s+(.*)', st)
        if m:
            if in_list: out.append('\\end{%s}' % in_list); in_list = None
            lvl = len(m.group(1))
            txt = re.sub(r'^\d+(\.\d+)*\.?\s*', '', m.group(2))
            txt = re.sub(r'^\u00a7\d+\s*', '', txt)
            txt = txt.replace('~', 'about ').replace('  ', ' ')   # no math in headings
            cmd = {1: 'section', 2: 'subsection', 3: 'subsubsection', 4: 'paragraph'}[lvl]
            lbl = ''
            if txt.strip() in ('Scope and Methodology', 'Scope and Corpus'):
                lbl = '\\label{sec:method}'
            elif 'Reproduction Study' in txt or 'Re-Evaluation' in txt or 'Re-evaluation' in txt:
                lbl = '\\label{sec:repro}'
            out.append('\\%s{%s}%s' % (cmd, convert_inline(txt), lbl))
            i += 1; continue
        m = re.match(r'^(\s*)([-*])\s+(.*)', ln)
        if m:
            if in_list != 'itemize':
                if in_list: out.append('\\end{%s}' % in_list)
                out.append('\\begin{itemize}'); in_list = 'itemize'
            out.append('  \\item ' + convert_inline(m.group(3))); i += 1; continue
        m = re.match(r'^(\s*)\d+\.\s+(.*)', ln)
        if m:
            if in_list != 'enumerate':
                if in_list: out.append('\\end{%s}' % in_list)
                out.append('\\begin{enumerate}'); in_list = 'enumerate'
            out.append('  \\item ' + convert_inline(m.group(2))); i += 1; continue
        # wrapped continuation of the current list item (indented, not a new marker)
        if in_list and re.match(r'^\s+\S', ln):
            out[-1] = out[-1].rstrip() + ' ' + convert_inline(st); i += 1; continue
        if in_list: out.append('\\end{%s}' % in_list); in_list = None
        out.append(convert_inline(st)); i += 1
    if in_list: out.append('\\end{%s}' % in_list)
    if in_code: out.append('\\end{verbatim}')
    return '\n'.join(out)

# ---------- generated table .tex ----------
def esc(s):
    s = (s.replace('\\', '\\textbackslash{}').replace('&', '\\&').replace('%', '\\%')
          .replace('_', '\\_').replace('#', '\\#').replace('~', '\\textasciitilde{}')
          .replace('^', '\\textasciicircum{}').replace('$', '\\$'))
    s = spell(uni(s))
    # TeX never breaks a line at '/' or '+' (only at hyphens and spaces), so a dense
    # table cell like "OPT/LLaMA/Qwen/DS" or "W+A+KV+sparsify" is one unbreakable token
    # that overflows its p{} column regardless of width. \allowbreak{} here must run last,
    # after the backslash-escaping above, or its own backslash gets double-escaped.
    s = s.replace('/', '/\\allowbreak{}').replace('+', '+\\allowbreak{}')
    # Citation-key remainders like "DoubleBinaryFactorization" (after the one hyphen in
    # "Anon2025-DoubleBinaryFactorization") are camelCase with no further break point;
    # allow a break at each lowercase/digit -> uppercase boundary.
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])', r'\\allowbreak{}', s)

def csv_longtable(path, caption, label, cols, colspec, headers, landscape=False, cite_col=None):
    # `headers` are plain-word display labels (never the raw snake_case CSV column
    # names - those are code/data-schema identifiers, not paper prose, and LaTeX also
    # cannot break a bare "weight_repr" onto a second line, which overflows a narrow
    # header cell into its neighbour). `landscape` wraps the table in landscape.sty so
    # wide multi-column data tables get the ~24cm of a4-landscape width instead of ~16cm
    # portrait; both are needed for a 8-9 column table at footnotesize.
    # `cite_col` names a column (must match an inventory id / bib key) whose cell is
    # emitted as \citet{...} rather than escaped text, so every enumerated corpus row is
    # traceable to the numbered bibliography and the reference list stays complete.
    rows = list(csv.reader(open(path, encoding='utf-8')))
    hdr = rows[0]
    idx = [hdr.index(c) for c in cols]
    cite_i = hdr.index(cite_col) if cite_col else None
    def cell(row, i):
        if i >= len(row):
            return ''
        if i == cite_i and row[i].strip():
            return r'\citet{%s}' % row[i].strip()
        return esc(row[i])
    # Keep columns justified (ragged-right p{} cells cannot compress a slightly-long line
    # and then protrude by a point or two). \hbadness=10000 silences the underfull-hbox
    # report that a one-word cell in a wide fixed column otherwise raises hundreds of
    # times; \hfuzz absorbs sub-point rounding; \emergencystretch lets dense cells relax.
    L = []
    if landscape:
        L.append(r'\begin{landscape}')
    L += [r'\begingroup\footnotesize\setlength{\tabcolsep}{4pt}'
          r'\hbadness=10000 \hfuzz=2pt \emergencystretch=3em',
         r'\begin{longtable}{%s}' % colspec,
         r'\caption{%s}\label{%s}\\' % (caption, label),
         r'\toprule ' + ' & '.join(headers) + r' \\ \midrule \endfirsthead',
         r'\toprule ' + ' & '.join(headers) + r' \\ \midrule \endhead',
         r'\bottomrule \endfoot']
    for row in rows[1:]:
        L.append(' & '.join(cell(row, i) for i in idx) + r' \\')
    L += [r'\end{longtable}', r'\endgroup']
    if landscape:
        L.append(r'\end{landscape}')
    return '\n'.join(L)

os.makedirs('tables', exist_ok=True)
T1 = csv_longtable(
 'data/inventory.csv',
 'Classification of the surveyed corpus on the taxonomy axes. '
 'Weight type, training paradigm, and quantized components each partition the '
 'corpus; their counts sum to 140. \\emph{Evidence basis} gives venue (\\emph{preprint} if '
 'not peer reviewed) and independent-check status (\\emph{ext.\\ repro} for an external '
 'one); it is not a graded score. In the cells: \\emph{n/a} = axis does not apply; '
 '\\emph{NA} = not applicable (activation-bit/systems-layer); \\emph{NR} = not reported; '
 '\\emph{var} = a range rather than one value.',
 'tab:classification',
 ['id', 'year', 'weight_repr', 'paradigm', 'components', 'act_bits', 'systems_layers', 'modality', 'basis'],
 r'p{3.2cm} p{1cm} p{1.9cm} p{2.2cm} p{2.2cm} p{1.3cm} p{2.2cm} p{2.1cm} p{2.5cm}',
 ['Reference', 'Year', 'Weight type', 'Training paradigm', 'Components quantized', 'Act. bits', 'Systems layer', 'Modality', 'Evidence basis'],
 landscape=True, cite_col='id')
T5 = csv_longtable(
 'data/results.csv',
 'Reported headline results (author-reported; a subset is independently re-measured '
 'elsewhere in this paper). '
 'Effective bits is the nominal code width unless marked \\emph{effective} (overhead-adjusted) '
 'or \\emph{var} (a range), following the accounting in Section~8.6. \\emph{Evidence basis} '
 'is venue plus independent-check status; it is not a graded score. '
 'Blank cells mean not reported.',
 'tab:results',
 ['id', 'model', 'scale', 'config', 'effective_bits', 'ppl_wikitext2', 'zeroshot_avg', 'mem', 'latency_or_speed', 'basis'],
 r'p{2.3cm} p{1.9cm} p{1.1cm} p{2.6cm} p{1.0cm} p{2.0cm} p{3.0cm} p{1.3cm} p{2.5cm} p{2.2cm}',
 ['Reference', 'Model', 'Scale', 'Configuration', 'Eff. bits', 'WikiText-2 ppl.', 'Zero-shot avg.', 'Memory', 'Latency / speed', 'Evidence basis'],
 landscape=True, cite_col='id')
# also emitted as standalone files for optional \input use; the main .tex inlines them (see AFTER) so it stays self-contained
open('tables/table1.tex', 'w', encoding='utf-8').write(T1)
open('tables/table5.tex', 'w', encoding='utf-8').write(T5)
print('tables written')

# ---------- pre-rendered native TikZ/pgfplots figures ----------
# Every pgfplots axis/bar/scatter figure below is written out here as a standalone .tex
# source (still recomputed from data/*.csv on every run, so nothing drifts from the
# corpus) and compiled separately to a PDF that the main document just \includegraphics's.
# This is what actually fixes slow/failing compiles on resource-limited services like
# Overleaf's free tier: pgfplots' per-figure coordinate and tick computation is the
# single biggest cost in compiling this document, and moving it out means the main
# document no longer loads pgfplots (or tikz) at all. The `geometry` line here must stay
# byte-identical to the main preamble's: it is what makes a pgfplots `width=0.6\textwidth`
# option resolve to the exact same absolute size here as it would embedded in the main
# document, even though `standalone` crops the final page to the content's bounding box.
_STANDALONE_GEOMETRY = r"\usepackage[a4paper,margin=0.85in]{geometry}"
def _standalone_tex(body, groupplots=False):
    pgf = ("\\usepackage{pgfplots}\n\\pgfplotsset{compat=1.16}\n"
           + ("\\usepgfplotslibrary{groupplots}\n" if groupplots else ''))
    return (r"""\documentclass[11pt,tikz,border={14pt 14pt 14pt 14pt}]{standalone}
""" + _STANDALONE_GEOMETRY + "\n" + r"""\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb}
""" + pgf + r"""\begin{document}
""" + body + r"""
\end{document}
""")
def write_standalone_fig(slug, body, groupplots=False):
    open(f'figures/fig-{slug}.tex', 'w', encoding='utf-8').write(_standalone_tex(body, groupplots))

# figure floats: plain \begin{figure}...\end{figure} blocks, one per figure asset in
# figures/ (found via \graphicspath in the preamble). No placeholder fallback: if a PDF
# is missing the build fails loudly at compile time rather than silently, which is the
# point once the figures are meant to be final rather than in-progress.
FIG1 = (r"""
\begin{figure}[htbp]
\centering
\includegraphics[width=\textwidth]{fig1-taxonomy.pdf}
\caption{Five-axis taxonomy of the surveyed corpus (135 in-window works plus five pre-2023 foundational works, listed in Table 1). Axes 1, 2, 3, and 5 partition all 140 works; axis 4 (optimization mechanism) is a non-exclusive tally and does not sum to 140. The modality cut at the bottom is a secondary partition.}
\label{fig:taxonomy}
\end{figure}
""")
FIGORG = (r"""
\begin{figure}[htbp]
\centering
\includegraphics[width=\textwidth]{fig-roadmap.pdf}
\caption{Organization of the paper as a tree, read in two columns left to right. The shaded branches are this paper's analytical contribution.}
\label{fig:roadmap}
\end{figure}
""")
FIG3 = (r"""
\begin{figure}[htbp]
\centering
\includegraphics[width=\textwidth]{fig3-timeline.pdf}
\caption{Timeline of native 1-bit and 1.58-bit LLM research, January 2023 to June 2026, organized by theme and by year. Entries are curated highlights, not the full corpus; the full classification is Table 1.}
\label{fig:timeline}
\end{figure}
""")
FIG4 = (r"""
\begin{figure}[htbp]
\centering
\includegraphics[width=\textwidth]{fig-datapath.pdf}
\caption{Three \texttt{BitLinear} datapath variants on a common template. Blue is the activation quantizer, orange the weight quantizer, and purple the ternary matrix multiplication, identical across all three. (a) BitLinear (BitNet b1.58): INT8 activations. (b) H-BitLinear (BitNet v2): an online Hadamard rotation (green) enables INT4 activations. (c) BitNet a4.8: well-behaved inputs go directly to INT4; outlier-heavy inputs are top-K sparsified (red) then quantized to INT8. All three retain a full-precision latent weight trained with a straight-through estimator.}
\label{fig:datapath}
\end{figure}
""")

# Fig: native pgfplots. The efficiency re-evaluation - BitNet i2_s vs Qwen2.5-1.5B at
# three quantisation levels, four threads, from Section 10.4 (Table in draft/09).
# BitNet in the accent colour; the Qwen baselines in a graded blue.
_body_efficiency_bars = r"""
\definecolor{bnAccent}{HTML}{D95F0E}
\definecolor{q4Blue}{HTML}{2166AC}
\definecolor{q8Blue}{HTML}{6BAED6}
\definecolor{f16Blue}{HTML}{C6DBEF}
\begin{tikzpicture}
\begin{groupplot}[
  group style={group size=2 by 2, horizontal sep=1.5cm, vertical sep=1.4cm},
  width=0.42\textwidth, height=4.6cm,
  ybar=0pt, enlarge x limits=0.28,
  symbolic x coords={BN,Q4,Q8,F16}, xtick={BN,Q4,Q8,F16},
  xticklabel style={font=\scriptsize}, yticklabel style={font=\scriptsize},
  title style={font=\small}, ymin=0, ymajorgrids, tick align=inside,
  every axis plot/.append style={draw=black!45, bar width=11pt},
]
\nextgroupplot[title={decode tok/s}, ymax=40]
  \addplot[fill=bnAccent] coordinates {(BN,28.6)};
  \addplot[fill=q4Blue]   coordinates {(Q4,33.8)};
  \addplot[fill=q8Blue]   coordinates {(Q8,24.1)};
  \addplot[fill=f16Blue]  coordinates {(F16,14.4)};
\nextgroupplot[title={prefill tok/s}, ymax=130]
  \addplot[fill=bnAccent] coordinates {(BN,108.9)};
  \addplot[fill=q4Blue]   coordinates {(Q4,107.6)};
  \addplot[fill=q8Blue]   coordinates {(Q8,72.4)};
  \addplot[fill=f16Blue]  coordinates {(F16,70.9)};
\nextgroupplot[title={disk (GiB)}, ymax=3.6]
  \addplot[fill=bnAccent] coordinates {(BN,1.10)};
  \addplot[fill=q4Blue]   coordinates {(Q4,1.04)};
  \addplot[fill=q8Blue]   coordinates {(Q8,1.76)};
  \addplot[fill=f16Blue]  coordinates {(F16,3.31)};
\nextgroupplot[title={peak RAM (GB)}, ymax=3.6]
  \addplot[fill=bnAccent] coordinates {(BN,1.22)};
  \addplot[fill=q4Blue]   coordinates {(Q4,1.60)};
  \addplot[fill=q8Blue]   coordinates {(Q8,1.64)};
  \addplot[fill=f16Blue]  coordinates {(F16,3.02)};
\end{groupplot}
\end{tikzpicture}"""
write_standalone_fig('efficiency-bars', _body_efficiency_bars, groupplots=True)

_body_efficiency_scatter = r"""
\definecolor{bnAccent}{HTML}{D95F0E}
\definecolor{q4Blue}{HTML}{2166AC}
\definecolor{q8Blue}{HTML}{6BAED6}
\definecolor{f16Blue}{HTML}{C6DBEF}
\begin{tikzpicture}
\begin{axis}[
  width=0.62\textwidth, height=5.0cm,
  xlabel={decode tok/s (higher is better)}, ylabel={peak RAM, GB (lower is better)},
  xlabel style={font=\scriptsize}, ylabel style={font=\scriptsize},
  xticklabel style={font=\scriptsize}, yticklabel style={font=\scriptsize},
  y dir=reverse, xmin=12, xmax=38, ymin=0.9, ymax=3.4,
  xmajorgrids, ymajorgrids, grid style={draw=black!12},
  axis line style={draw=black!45}, tick align=inside,
]
\addplot[only marks, mark=*, mark size=2.6pt, color=bnAccent, mark options={draw=black!40}] coordinates {(28.6,1.22)};
\addplot[only marks, mark=*, mark size=2.6pt, color=q4Blue,   mark options={draw=black!40}] coordinates {(33.8,1.60)};
\addplot[only marks, mark=*, mark size=2.6pt, color=q8Blue,   mark options={draw=black!40}] coordinates {(24.1,1.64)};
\addplot[only marks, mark=*, mark size=2.6pt, color=f16Blue,  mark options={draw=black!40}] coordinates {(14.4,3.02)};
\node[anchor=south, font=\scriptsize] at (axis cs:28.6,1.22) {BN};
\node[anchor=north, font=\scriptsize] at (axis cs:33.8,1.60) {Q4};
\node[anchor=south, font=\scriptsize] at (axis cs:24.1,1.64) {Q8};
\node[anchor=north, font=\scriptsize] at (axis cs:14.4,3.02) {F16};
\end{axis}
\end{tikzpicture}"""
write_standalone_fig('efficiency-scatter', _body_efficiency_scatter)

FIG5 = (r"""
\begin{figure}[htbp]
\centering
\includegraphics{fig-efficiency-bars.pdf}

\vspace{3mm}
\includegraphics{fig-efficiency-scatter.pdf}
\caption{Independent efficiency re-evaluation on one x86 laptop: decode throughput (mean of five repeats at a common four-thread point), on-disk size (exact), and peak resident memory (a single sample at eight threads, essentially thread-independent). BN (orange) is the BitNet b1.58 2B4T \texttt{I2\_S} checkpoint; Q4, Q8, and F16 (blues) are Qwen2.5-1.5B-Instruct at \texttt{Q4\_K\_M}, \texttt{Q8\_0}, and FP16. The bottom panel plots decode throughput against peak memory: BitNet and Q4 share the Pareto frontier, while Q8 and F16 are dominated on both axes.}
\label{fig:efficiency}
\end{figure}
""")

# Fig: native pgfplots. In-window corpus by year, stacked by evidence basis (Section 3.3),
# computed directly from data/inventory.csv so it never drifts from Table 1 / the
# corpus-assembly funnel (Section 3.2) or the corroborated-works count of Section 3.3.
_year_basis = {}
for _r in inv.values():
    _y = _r['year'].strip()
    if _y.isdigit() and int(_y) >= 2023:
        _yb = _year_basis.setdefault(_y, {'yes': 0, 'no': 0})
        _yb['yes' if _r['corroborated'].strip() == 'yes' else 'no'] += 1
_years_sorted = sorted(_year_basis)
_year_yes = ' '.join(f'({y},{_year_basis[y]["yes"]})' for y in _years_sorted)
_year_no = ' '.join(f'({y},{_year_basis[y]["no"]})' for y in _years_sorted)
_year_total_max = max(_year_basis[y]['yes'] + _year_basis[y]['no'] for y in _years_sorted)
_body_growth = r"""
\definecolor{growthCorrob}{HTML}{2166AC}
\definecolor{growthPreprint}{HTML}{C6DBEF}
\begin{tikzpicture}
\begin{axis}[
  width=0.6\textwidth, height=5.2cm,
  ybar stacked, bar width=28pt,
  symbolic x coords={""" + ','.join(_years_sorted) + r"""},
  xtick=data, xticklabel style={font=\small},
  yticklabel style={font=\small},
  ylabel={works included}, ylabel style={font=\small},
  ymin=0, ymax=""" + str(_year_total_max + 12) + r""", ymajorgrids, tick align=inside,
  enlarge x limits=0.2, axis line style={draw=black!45}, grid style={draw=black!10},
  legend style={font=\scriptsize, at={(0.02,0.97)}, anchor=north west, draw=black!30},
  legend cell align=left,
]
\addplot[fill=growthCorrob, draw=black!45] coordinates {""" + _year_yes + r"""};
\addlegendentry{corroborated}
\addplot[fill=growthPreprint, draw=black!45] coordinates {""" + _year_no + r"""};
\addlegendentry{single preprint}
\end{axis}
\end{tikzpicture}"""
write_standalone_fig('growth', _body_growth)
FIGGROWTH = (r"""
\begin{figure}[htbp]
\centering
\includegraphics{fig-growth.pdf}
\caption{In-window corpus by year of first publication, stacked by evidence basis: corroborated means peer reviewed or with an independent check; the rest are single unreproduced preprints. 135 primary studies, January 2023 to June 2026 (2026 is a partial year, through the June cutoff). The falling corroborated share in recent years partly reflects review lag, not only falling scrutiny.}
\label{fig:growth}
\end{figure}
""")

# Fig: native TikZ heat-grid. Weight representation x training paradigm, the cross-tabulation
# behind Section 4.7's reading of the taxonomy ("native training has concentrated on ternary
# weights while binary has remained largely a post-training target"). Computed directly from
# data/inventory.csv; restricted to the four paradigms that partition the axis (Section 4.2)
# and the three weight types that carry a training paradigm at all (Section 4.1).
_heat_paradigms = ['native-scratch', 'continual-QAT', 'QAT-finetune', 'PTQ']
_heat_weights = ['binary', 'ternary', 'mixed-partial']
_heat_counts = {w: {p: 0 for p in _heat_paradigms} for w in _heat_weights}
for _r in inv.values():
    _w, _p = _r['weight_repr'].strip(), _r['paradigm'].strip()
    if _w in _heat_counts and _p in _heat_paradigms:
        _heat_counts[_w][_p] += 1
_heat_max = max(v for row in _heat_counts.values() for v in row.values())
_heat_col_disp = {'native-scratch': 'native', 'continual-QAT': 'cont.QAT', 'QAT-finetune': 'QAT-FT', 'PTQ': 'PTQ'}
_CW, _CH = 2.5, 0.95
_heat_cells = []
for _ri, _w in enumerate(_heat_weights):
    _y0 = -_ri * _CH
    _heat_cells.append(f"\\node[font=\\small, anchor=east] at (-0.15,{_y0 - _CH/2:.2f}) {{{_w}}};")
    for _ci, _p in enumerate(_heat_paradigms):
        _v = _heat_counts[_w][_p]
        _pct = max(12, round(100 * _v / _heat_max))
        _tc = 'white' if _pct > 55 else 'black'
        _x0 = _ci * _CW
        _heat_cells.append(
            f"\\fill[heatBlue!{_pct}!white] ({_x0:.2f},{_y0:.2f}) rectangle ++({_CW:.2f},{-_CH:.2f});"
            f" \\node[{_tc}, font=\\small] at ({_x0 + _CW/2:.2f},{_y0 - _CH/2:.2f}) {{{_v}}};"
        )
for _ci, _p in enumerate(_heat_paradigms):
    _heat_cells.append(f"\\node[font=\\scriptsize] at ({_ci*_CW + _CW/2:.2f},{0.55:.2f}) {{{_heat_col_disp[_p]}}};")
_body_heatmap = r"""
\definecolor{heatBlue}{HTML}{2166AC}
\begin{tikzpicture}[x=1cm, y=1cm]
""" + '\n'.join(_heat_cells) + r"""
\end{tikzpicture}"""
write_standalone_fig('heatmap', _body_heatmap)
FIGHEATMAP = (r"""
\begin{figure}[htbp]
\centering
\includegraphics{fig-heatmap.pdf}
\caption{Weight representation against training paradigm, restricted to the three weight types and four paradigms that carry a training procedure (systems, analysis, and survey works are excluded). Native training concentrates on ternary (18 of 27 native works); post-training quantization concentrates on binary (16 of 27 PTQ works).}
\label{fig:heatmap}
\end{figure}
""")

# Fig: native pgfplots. Reported vs. effective bits per weight (Section 8.6): where a strict
# accounting is available in the text, the headline figure understates real storage.
_body_effbits = r"""
\definecolor{bitsAccent}{HTML}{D95F0E}
\definecolor{bitsGray}{HTML}{94A3B8}
\definecolor{bitsDark}{HTML}{334155}
\begin{tikzpicture}
\begin{axis}[
  width=0.85\textwidth, height=8.4cm,
  xlabel={bits per weight}, xlabel style={font=\small},
  xmin=0.5, xmax=4.5, xmajorgrids, grid style={draw=black!10},
  symbolic y coords={STBLLM,BiLLM,RaBiT,PB-LLM,PTQ1.61,{Native ternary},ARB-LLM},
  ytick={STBLLM,BiLLM,RaBiT,PB-LLM,PTQ1.61,{Native ternary},ARB-LLM},
  hide obscured y ticks=false, yticklabel style={font=\small}, y dir=reverse,
  tick align=outside, axis line style={draw=black!45},
  legend style={font=\scriptsize, at={(0.98,0.03)}, anchor=south east, draw=black!30},
  legend cell align=left,
]
\addplot[only marks, mark=*, mark size=2.2pt, color=bitsGray] coordinates {(1.08,BiLLM) (2.0,RaBiT)};
\addlegendentry{reported (headline)}
\addplot[only marks, mark=*, mark size=2.6pt, color=bitsDark] coordinates {(2.88,BiLLM) (2.02,RaBiT) (1.1,ARB-LLM) (1.61,PTQ1.61) (1.70,PB-LLM) (4.13,STBLLM)};
\addlegendentry{effective (strict accounting)}
\addplot[only marks, mark=*, mark size=2.8pt, color=bitsAccent] coordinates {(1.58,{Native ternary})};
\addlegendentry{native ternary (genuine)}
\draw[bitsGray] (axis cs:1.08,BiLLM) -- (axis cs:2.88,BiLLM);
\draw[bitsGray] (axis cs:2.0,RaBiT) -- (axis cs:2.02,RaBiT);
\end{axis}
\end{tikzpicture}"""
write_standalone_fig('effbits', _body_effbits)
FIGBITS = (r"""
\begin{figure}[htbp]
\centering
\includegraphics{fig-effbits.pdf}
\caption{Reported versus effective bits per weight. Where a strict accounting exists, the headline figure (grey) understates real storage against the effective one (dark): BiLLM's 1.08 becomes 2.88, RaBiT's nominal two bits becomes 2.02. ARB-LLM, PTQ1.61, PB-LLM, and STBLLM report only one figure. Native ternary (orange) has no such accounting gap between a deflated headline and its real storage cost: 1.58 is both nominal and effective. That is a separate question from the packed format a given kernel actually uses on disk, which for I2\_S is two bits per weight for hardware convenience, not an overhead the accounting here is missing.}
\label{fig:effbits}
\end{figure}
""")

# Fig: native pgfplots. The three controlled accuracy pairs of Table tab:acc-controlled
# (Section 10.3), as a dumbbell chart, in decreasing order of how tightly matched each pair is.
_body_controlledpairs = r"""
\definecolor{ctrlOrange}{HTML}{D95F0E}
\definecolor{ctrlBlue}{HTML}{2166AC}
\begin{tikzpicture}
\begin{axis}[
  width=0.85\textwidth, height=4.6cm,
  xlabel={seven-task zero-shot mean accuracy}, xlabel style={font=\small},
  xmin=42, xmax=63, xmajorgrids, grid style={draw=black!10},
  symbolic y coords={{Falcon3-1B (1.58-bit vs bf16)},{Qwen2.5-1.5B (nf4 vs bf16)},{Spectra 2.4B (ternary vs FP16)}},
  ytick=data, yticklabel style={font=\small}, y dir=reverse,
  axis line style={draw=black!45}, tick align=outside,
  legend style={font=\scriptsize, at={(0.98,0.97)}, anchor=north east, draw=black!30},
  legend cell align=left,
]
\addplot[only marks, mark=*, mark size=3pt, color=ctrlOrange] coordinates {(45.69,{Falcon3-1B (1.58-bit vs bf16)}) (57.33,{Qwen2.5-1.5B (nf4 vs bf16)}) (51.49,{Spectra 2.4B (ternary vs FP16)})};
\addlegendentry{ternary / 4-bit}
\addplot[only marks, mark=*, mark size=3pt, color=ctrlBlue] coordinates {(57.22,{Falcon3-1B (1.58-bit vs bf16)}) (60.00,{Qwen2.5-1.5B (nf4 vs bf16)}) (52.05,{Spectra 2.4B (ternary vs FP16)})};
\addlegendentry{full precision}
\draw[black!40] (axis cs:45.69,{Falcon3-1B (1.58-bit vs bf16)}) -- (axis cs:57.22,{Falcon3-1B (1.58-bit vs bf16)});
\draw[black!40] (axis cs:57.33,{Qwen2.5-1.5B (nf4 vs bf16)}) -- (axis cs:60.00,{Qwen2.5-1.5B (nf4 vs bf16)});
\draw[black!40] (axis cs:51.49,{Spectra 2.4B (ternary vs FP16)}) -- (axis cs:52.05,{Spectra 2.4B (ternary vs FP16)});
\end{axis}
\end{tikzpicture}"""
write_standalone_fig('controlledpairs', _body_controlledpairs)
FIGDUMBBELL = (r"""
\begin{figure}[htbp]
\centering
\includegraphics{fig-controlledpairs.pdf}
\caption{The three controlled pairs of Table~\ref{tab:acc-controlled}: seven-task zero-shot mean for each ternary or 4-bit model (orange) against its full-precision counterpart (blue), in decreasing order of match quality. The Spectra pair lands within 0.6 points; the least-matched Falcon3-1B pair loses 11.5.}
\label{fig:controlledpairs}
\end{figure}
""")

# Fig: plain TikZ, no data (didactic). The straight-through estimator (Section 2.3 / 6.3):
# the quantizer used in the forward pass and the clipped-identity gradient substituted for
# its true (almost-everywhere-zero) gradient in the backward pass.
_body_ste = r"""
\definecolor{steAccent}{HTML}{D95F0E}
\definecolor{steDark}{HTML}{334155}
\begin{tikzpicture}[scale=1]
\draw[->] (-2.3,0) -- (2.3,0) node[right, font=\scriptsize] {$w$};
\draw[->] (0,-1.6) -- (0,1.6) node[above, font=\scriptsize] {$q(w)$};
\draw[thick, color=steAccent] (-2,-1) -- (-0.5,-1);
\draw[thick, color=steAccent] (-0.5,0) -- (0.5,0);
\draw[thick, color=steAccent] (0.5,1) -- (2,1);
\draw[dashed, color=black!40] (-0.5,-1) -- (-0.5,0);
\draw[dashed, color=black!40] (0.5,0) -- (0.5,1);
\node[font=\scriptsize] at (-1.7,-1.3) {$-1$};
\node[font=\scriptsize] at (1.7,1.3) {$+1$};
\node[font=\scriptsize] at (0,-2.15) {(a) forward pass: the quantizer $q(w)$};
\begin{scope}[xshift=6.2cm]
\draw[->] (-2.3,0) -- (2.3,0) node[right, font=\scriptsize] {$w$};
\draw[->] (0,-0.3) -- (0,1.6) node[above, font=\scriptsize] {gradient};
\draw[thick, densely dotted, color=black!55] (-2.1,0.05) -- (2.1,0.05);
\draw[thick, color=steDark] (-2,0) -- (-1,0) -- (-1,1) -- (1,1) -- (1,0) -- (2,0);
\node[font=\scriptsize, color=steDark, anchor=west] at (0.15,1.15) {STE gradient (used)};
\node[font=\scriptsize, color=black!55, anchor=west] at (1.15,0.32) {true gradient $\approx 0$ a.e.};
\node[font=\scriptsize] at (0,-1.0) {(b) backward pass: straight-through estimator};
\end{scope}
\end{tikzpicture}"""
write_standalone_fig('ste', _body_ste)
FIGSTE = (r"""
\begin{figure}[htbp]
\centering
\includegraphics{fig-ste.pdf}
\caption{The straight-through estimator. (a) The forward-pass quantizer, here the ternary rule with thresholds at $\pm 0.5$ of the normalized weight $w$, is piecewise constant with zero true gradient almost everywhere. (b) The backward pass instead propagates a clipped-identity gradient (dark), letting the full-precision shadow weight update despite the quantizer's own zero gradient.}
\label{fig:ste}
\end{figure}
""")

# Fig: native pgfplots, 100%-stacked bar. Weight-representation share by year, computed
# directly from data/inventory.csv (Section 4.7): binary's share of new work has fallen
# since 2024 while ternary has stayed the largest or second-largest category throughout.
_wy_types = ['ternary', 'binary', 'mixed-partial', 'n/a']
_wy_counts = {}
for _r in inv.values():
    _y = _r['year'].strip()
    if _y.isdigit() and int(_y) >= 2023:
        _wt = _r['weight_repr'].strip() or 'n/a'
        _row = _wy_counts.setdefault(_y, {t: 0 for t in _wy_types})
        _row[_wt] += 1
_wy_years = sorted(_wy_counts)
_wy_pct = {y: {t: 100.0 * _wy_counts[y][t] / sum(_wy_counts[y].values()) for t in _wy_types} for y in _wy_years}
_wy_colors = {'ternary': 'wyTernary', 'binary': 'wyBinary', 'mixed-partial': 'wyMixed', 'n/a': 'wyNA'}
_wy_plots = []
for _t in _wy_types:
    _coords = ' '.join(f'({y},{_wy_pct[y][_t]:.1f})' for y in _wy_years)
    _wy_plots.append(f"\\addplot[fill={_wy_colors[_t]}, draw=black!45] coordinates {{{_coords}}};\n\\addlegendentry{{{_t}}}")
_body_weightyear = r"""
\definecolor{wyTernary}{HTML}{2166AC}
\definecolor{wyBinary}{HTML}{D95F0E}
\definecolor{wyMixed}{HTML}{6BAED6}
\definecolor{wyNA}{HTML}{C6DBEF}
\begin{tikzpicture}
\begin{axis}[
  width=0.6\textwidth, height=5.2cm,
  ybar stacked, bar width=28pt,
  symbolic x coords={""" + ','.join(_wy_years) + r"""},
  xtick=data, xticklabel style={font=\small},
  yticklabel style={font=\small}, ylabel={share of works (\%)}, ylabel style={font=\small},
  ymin=0, ymax=115, ytick={0,20,40,60,80,100}, ymajorgrids, tick align=inside,
  enlarge x limits=0.25, axis line style={draw=black!45}, grid style={draw=black!10},
  legend style={font=\scriptsize, at={(0.5,1.12)}, anchor=south, legend columns=4, draw=black!30},
  legend cell align=left,
]
""" + '\n'.join(_wy_plots) + r"""
\end{axis}
\end{tikzpicture}"""
write_standalone_fig('weightyear', _body_weightyear)
FIGWEIGHTYEAR = (r"""
\begin{figure}[htbp]
\centering
\includegraphics{fig-weightyear.pdf}
\caption{Weight-representation share by year, each bar normalized to 100\% of that year's works. Binary peaked at a third of new work in 2024 and fell to under a tenth by 2026; ternary stayed largest or second-largest throughout. 2023 (four works) and 2026 (partial year) should be read cautiously.}
\label{fig:weightyear}
\end{figure}
""")

# Fig: plain TikZ Euler diagram (not area-proportional), the systems-stack axis (Section
# 4.5 / 7.4): how many works co-design across algorithm, kernel, and hardware, computed
# directly from data/inventory.csv's systems_layers column.
_sl = {}
for _r in inv.values():
    _sl[_r['systems_layers'].strip()] = _sl.get(_r['systems_layers'].strip(), 0) + 1
_body_systemsvenn = r"""
\definecolor{vennAlgo}{HTML}{2166AC}
\definecolor{vennKernel}{HTML}{D95F0E}
\definecolor{vennHW}{HTML}{1BAF7A}
\begin{tikzpicture}[font=\small]
\draw[fill=vennAlgo, opacity=0.32, draw=vennAlgo!70!black, thick] (-1,1) circle (1.8);
\draw[fill=vennKernel, opacity=0.32, draw=vennKernel!70!black, thick] (1,1) circle (1.8);
\draw[fill=vennHW, opacity=0.32, draw=vennHW!70!black, thick] (0,-0.9) circle (1.8);
\node[font=\bfseries] at (-2.5,2.7) {algorithm};
\node[font=\bfseries] at (2.5,2.7) {kernel};
\node[font=\bfseries] at (0,-3.0) {hardware};
\node at (-2.1,1.9) {""" + str(_sl.get('algorithm', 0)) + r"""};
\node at (2.1,1.9) {""" + str(_sl.get('kernel', 0)) + r"""};
\node at (0,-2.3) {""" + str(_sl.get('hardware', 0)) + r"""};
\node at (0,1.55) {""" + str(_sl.get('algo+kernel', 0)) + r"""};
\node at (-1.05,-0.55) {""" + str(_sl.get('algo+hw', 0)) + r"""};
\node at (1.05,-0.55) {""" + str(_sl.get('kernel+hw', 0)) + r"""};
\node[font=\bfseries] at (0,0.35) {""" + str(_sl.get('algo+kernel+hw', 0)) + r"""};
\node[font=\scriptsize] at (0,-4.0) {(""" + str(_sl.get('NA', 0)) + r""" survey works with no systems-stack contribution are not pictured)};
\end{tikzpicture}"""
write_standalone_fig('systemsvenn', _body_systemsvenn)
FIGVENN = (r"""
\begin{figure}[htbp]
\centering
\includegraphics{fig-systemsvenn.pdf}
\caption{How far down the stack the corpus reaches: co-occurrence of algorithm, kernel, and hardware contributions; areas are illustrative, not proportional to count. Ninety-five works are algorithm only; only five co-design across all three layers.}
\label{fig:systemsvenn}
\end{figure}
""")

ORDER = ['01-introduction', '02-background', '03-methodology', '04-taxonomy', '05-architecture',
         '06-training', '07-systems', '07b-benchmarking', '08-applications', '09-reproduction',
         '10-open-problems', '11-conclusion']
AFTER = {
 '01-introduction': '\n' + FIGORG + '\n' + FIG3 + '\n',
 '02-background': '\n' + FIGSTE + '\n',
 '03-methodology': '\n' + FIGGROWTH + '\n',
 '04-taxonomy': '\n' + FIG1 + '\n' + FIGHEATMAP + '\n' + FIGWEIGHTYEAR + '\n' + T1 + '\n',
 '05-architecture': '\n' + FIG4 + '\n',
 '07-systems': '\n' + FIGVENN + '\n',
 '07b-benchmarking': '\n\n' + T5 + '\n' + FIGBITS + '\n',
 '09-reproduction': '\n' + FIGDUMBBELL + '\n' + FIG5 + '\n',
}
PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[a4paper,margin=0.85in]{geometry}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb,textcomp}
\usepackage{booktabs,longtable,array,tabularx}
\newcolumntype{L}{>{\raggedright\arraybackslash}X}
\usepackage{pdflscape}
\usepackage{graphicx}
\usepackage[numbers,sort&compress]{natbib}
\usepackage{hyperref}
\hypersetup{
  colorlinks=true, linkcolor=black, citecolor=black, urlcolor=blue,
  pdftitle={Native 1-Bit and 1.58-Bit Large Language Models: A Survey and an Independent Re-Evaluation},
  pdfauthor={Habib Ullah Manzoor and Basim Alhumaily},
  pdfsubject={Survey and independent re-evaluation of native 1-bit and 1.58-bit large language models},
  pdfkeywords={1-bit language models, 1.58-bit language models, BitNet, quantization-aware training, efficient inference, hardware co-design}
}
\usepackage{microtype}
\usepackage{caption}
\usepackage{authblk}
\captionsetup{font=small,labelfont=bf,skip=4pt}
\graphicspath{{figures/}}
\setcounter{secnumdepth}{3}
\title{Native 1-Bit and 1.58-Bit Large Language Models:\\[2pt]
       A Survey and an Independent Re-Evaluation}
\author[1]{Habib Ullah Manzoor\thanks{Corresponding author. Email: \texttt{habib.manzoor@uws.ac.uk}}}
\author[2]{Basim Alhumaily\thanks{Email: \texttt{b.alhumaily@qu.edu.sa}}}
\affil[1]{School of Computing, Engineering and Physical Sciences, University of the West of Scotland, UK}
\affil[2]{Department of Electrical Engineering, College of Engineering, Qassim University, Buraydah 52571, Saudi Arabia}
\date{}
\begin{document}
\maketitle
\begin{abstract}
\noindent Large language models whose linear-layer weights are constrained to
binary $\{-1,+1\}$ or ternary $\{-1,0,+1\}$ turn the dominant matrix
multiplication into addition. The centre of gravity is the native paradigm, which
imposes that constraint during training; adjacent post-training and
quantization-aware routes target the same one-to-two-bit range. This paper is a curated,
open-access survey of 135 works from 2023 to 2026, organized on a taxonomy and a common
effective-bits accounting, together with an independent re-measurement of the flagship
open model's headline claims and, where open matched checkpoints exist, a controlled test
of the accuracy claim. In a matched comparison, a native ternary model against its FP16
counterpart at the same parameter count, tokenizer, and training data, the two land
within 0.6 points on a seven-task zero-shot suite at the two-billion-parameter scale,
with the ternary model's perplexity about 14\% higher: downstream parity, worse
language-modeling loss. Post-hoc 4-bit quantization of a full-precision model loses more
of the suite than that, and a 1.58-bit model at the one-billion-parameter scale loses
much more; this is consistent with, but too thin a basis alone to establish, a scale
dependence for the parity result, and whether it holds beyond the measured regime is
untested. On efficiency the finding is pointed: on
one commodity x86 machine a standard 4-bit quantization of the full-precision baseline
matched or beat the flagship 1-bit model on decode speed and on-disk size and was
comparable on per-token energy, and held close on the accuracy tasks checked, leaving the
1-bit model only a 24-to-27\% smaller resident set; its efficiency case at this scale
holds against half precision and an 8-bit baseline but not against 4-bit, and a GPU and a
second machine are untested. The reference CPU
runtime, moreover, does not run the flagship model correctly as documented, needing a
one-line activation fix, a sign the open deployment path is still immature. The
activation-precision floor and training stability at frontier scale remain the field's
open problems.
\end{abstract}

\noindent\textbf{Index Terms:} 1-bit and 1.58-bit language models, BitNet,
quantization-aware training, efficient inference, hardware co-design.
\medskip
"""
body = []
for name in ORDER:
    tag = '07b' if name.startswith('07b') else name.split('-')[0]
    body.append('\n%% ===== ' + name + '\n' + convert_file(os.path.join('draft', name + '.md'), tag))
    if name in AFTER:
        body.append(AFTER[name])
DECLARATION = (r"""

\section*{Declaration of Generative AI and AI-Assisted Technologies in the Writing Process}

During the preparation of this work, the authors used Claude (Anthropic) to assist with
literature search support, drafting and editing manuscript text, generating figures from
author-specified content and data, and scripting the independent reproduction experiments
in Section~\ref{sec:repro}. The reported measurements were produced by running the cited
third-party software and released model checkpoints directly, not by the AI assistant.
All AI-assisted output was reviewed and verified by the authors, who take full
responsibility for the content and conclusions of this manuscript.
""")
TAIL = (DECLARATION +
        '\n\n\\bibliographystyle{unsrtnat}  %% numbered in ascending order of first citation\n'
        '\\bibliography{references}\n\\end{document}\n')
doc = PREAMBLE + '\n'.join(body) + TAIL

# --- global tidy passes ---
# merge adjacent \cite commands that ended up split across a wrapped line
for _ in range(4):
    doc = re.sub(r'\\cite\{([^}]+)\}[ \t]*\n?[ \t]*\\cite\{([^}]+)\}', r'\\cite{\1,\2}', doc)
# pull a stray line-leading punctuation mark back onto the previous line (from deleted placeholders / wrapped cites)
doc = re.sub(r'\}\s*\n[ \t]*([,.;:])', r'}\1\n', doc)
doc = re.sub(r'(?<=\S)\s*\n[ \t]*([,.;:])\s', r'\1 ', doc)
# "Section (\S 3)" style leftovers -> "Section 3"
doc = doc.replace('Section (\\S\\ref', 'Section~\\ref').replace('(\\S\\ref{', '\\ref{')
doc = re.sub(r'Section\s+\(?\\ref\{', r'Section~\\ref{', doc)
# tidy space-before-punctuation and 3+ spaces introduced by substitutions
doc = re.sub(r' {3,}', ' ', doc)
doc = re.sub(r'(?<=\S) +([,.;:)])', r'\1', doc)
doc = doc.replace('(Section 9); .', '(Section 9).').replace('; .', '.')
# straight double quotes that spanned a line break (missed by the per-line pass)
doc = re.sub(r'"([^"\n]*(?:\n[^"\n]*)?)"', lambda m: "``" + m.group(1) + "''", doc)

open('1bit-llm-survey.tex', 'w', encoding='utf-8').write(doc)
print('1bit-llm-survey.tex:', os.path.getsize('1bit-llm-survey.tex'), 'bytes')
