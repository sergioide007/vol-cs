# Appends Vol2-specific entries to a combined bib
entries = r"""
@misc{bai2022,
  author = {Bai, Yuntao and Kadavath, Saurav and Kundu, Sandipan and others},
  title = {Constitutional AI: Harmlessness from AI Feedback},
  year = {2022}, note = {Anthropic, arXiv preprint}
}
@misc{berner2019,
  author = {Berner, Christopher and Brockman, Greg and Chan, Brooke and others},
  title = {Dota 2 with Large Scale Deep Reinforcement Learning},
  year = {2019}, note = {OpenAI Five, arXiv preprint}
}
@inproceedings{blattmann2023,
  author = {Blattmann, Andreas and Rombach, Robin and Ling, Huan and others},
  title = {Align Your Latents: High-Resolution Video Synthesis with Latent Diffusion Models},
  booktitle = {CVPR}, year = {2023}
}
@misc{boner2014,
  author = {Bon{\'e}r, Jonas and Farley, Dave and Kuhn, Roland and Thompson, Martin},
  title = {The Reactive Manifesto},
  year = {2014}
}
@article{bovens2007,
  author = {Bovens, Mark},
  title = {Analysing and Assessing Accountability: A Conceptual Framework},
  journal = {European Law Journal}, year = {2007}
}
@inproceedings{brewer2000,
  author = {Brewer, Eric A.},
  title = {Towards Robust Distributed Systems (CAP Theorem)},
  booktitle = {ACM PODC}, year = {2000}
}
@inproceedings{colledanchise2018,
  author = {Colledanchise, Michele and {\"O}gren, Petter},
  title = {Behavior Trees in Robotics and AI: An Introduction},
  publisher = {CRC Press}, year = {2018}
}
@inproceedings{dettmers2023,
  author = {Dettmers, Tim and Pagnoni, Artidoro and Holtzman, Ari and Zettlemoyer, Luke},
  title = {{QLoRA}: Efficient Finetuning of Quantized LLMs},
  booktitle = {NeurIPS}, year = {2023}
}
@article{flp1985,
  author = {Fischer, Michael J. and Lynch, Nancy A. and Paterson, Michael S.},
  title = {Impossibility of Distributed Consensus with One Faulty Process},
  journal = {Journal of the ACM (JACM)}, year = {1985}
}
@book{forsgren2018,
  author = {Forsgren, Nicole and Humble, Jez and Kim, Gene},
  title = {Accelerate: The Science of Lean Software and DevOps},
  publisher = {IT Revolution Press}, year = {2018}
}
@misc{hewitt1973,
  author = {Hewitt, Carl and Bishop, Peter and Steiger, Richard},
  title = {A Universal Modular Actor Formalism for Artificial Intelligence},
  year = {1973}, note = {IJCAI}
}
@inproceedings{howard2019,
  author = {Howard, Andrew and Sandler, Mark and Chu, Grace and others},
  title = {Searching for {MobileNetV3}},
  booktitle = {ICCV}, year = {2019}
}
@book{hunt2019,
  author = {Hunt, Andrew and Thomas, David},
  title = {The Pragmatic Programmer},
  edition = {20th Anniversary}, publisher = {Addison-Wesley}, year = {2019}
}
@book{hutchins1995,
  author = {Hutchins, Edwin},
  title = {Cognition in the Wild},
  publisher = {MIT Press}, year = {1995}
}
@book{kleppmann2017,
  author = {Kleppmann, Martin},
  title = {Designing Data-Intensive Applications},
  publisher = {O'Reilly Media}, year = {2017}
}
@inproceedings{kwon2023,
  author = {Kwon, Woosuk and Li, Zhuohan and Zhuang, Siyuan and others},
  title = {Efficient Memory Management for Large Language Model Serving with {PagedAttention}},
  booktitle = {ACM SOSP}, year = {2023}
}
@article{lamport1982,
  author = {Lamport, Leslie and Shostak, Robert and Pease, Marshall},
  title = {The Byzantine Generals Problem},
  journal = {ACM Transactions on Programming Languages and Systems}, year = {1982}
}
@misc{mehta2021,
  author = {Mehta, Sachin and Rastegari, Mohammad},
  title = {{MobileViT}: Light-weight, General-purpose, and Mobile-friendly Vision Transformer},
  year = {2021}, note = {arXiv preprint}
}
@article{miller1956,
  author = {Miller, George A.},
  title = {The Magical Number Seven, Plus or Minus Two},
  journal = {Psychological Review}, year = {1956}
}
@book{millington2009,
  author = {Millington, Ian and Funge, John},
  title = {Artificial Intelligence for Games},
  edition = {2nd}, publisher = {CRC Press}, year = {2009}
}
@book{newman2019,
  author = {Newman, Sam},
  title = {Monolith to Microservices},
  publisher = {O'Reilly Media}, year = {2019}
}
@book{nygard2018,
  author = {Nygard, Michael T.},
  title = {Release It! Design and Deploy Production-Ready Software},
  edition = {2nd}, publisher = {Pragmatic Bookshelf}, year = {2018}
}
@article{saltzer1975,
  author = {Saltzer, Jerome H. and Schroeder, Michael D.},
  title = {The Protection of Information in Computer Systems},
  journal = {Proceedings of the IEEE}, year = {1975}
}
@article{tenenbaum2011,
  author = {Tenenbaum, Joshua B. and Kemp, Charles and Griffiths, Thomas L. and Goodman, Noah D.},
  title = {How to Grow a Mind: Statistics, Structure, and Abstraction},
  journal = {Science}, year = {2011}
}
@article{vinyals2019,
  author = {Vinyals, Oriol and Babuschkin, Igor and Czarnecki, Wojciech M. and others},
  title = {Grandmaster Level in {StarCraft II} Using Multi-Agent Reinforcement Learning},
  journal = {Nature}, year = {2019}
}
@misc{vogels2008,
  author = {Vogels, Werner},
  title = {Eventually Consistent},
  year = {2008}, note = {ACM Queue}
}
@article{witmer1998,
  author = {Witmer, Bob G. and Singer, Michael J.},
  title = {Measuring Presence in Virtual Environments: A Presence Questionnaire},
  journal = {Presence: Teleoperators and Virtual Environments}, year = {1998}
}
@misc{yao2022webshop,
  author = {Yao, Shunyu and Chen, Howard and Yang, John and Narasimhan, Karthik},
  title = {{WebShop}: Towards Scalable Real-World Web Interaction with Grounded Language Agents},
  year = {2022}, note = {NeurIPS}
}
@misc{defossez2022,
  author = {D{\'e}fossez, Alexandre and Copet, Jade and Synnaeve, Gabriel and Adi, Yossi},
  title = {High Fidelity Neural Audio Compression (EnCodec)},
  year = {2022}, note = {arXiv:2210.13438}
}
@misc{deepseek2024,
  author = {{DeepSeek AI}}, title = {Technical documentation, as cited in the manuscript}, year = {2024}
}
@misc{deepseek2025,
  author = {{DeepSeek AI}}, title = {Technical documentation, as cited in the manuscript}, year = {2025}
}
@misc{google2024,
  author = {{Google}}, title = {Technical documentation, as cited in the manuscript}, year = {2024}
}
@misc{googledeepmind2024,
  author = {{Google DeepMind}}, title = {Technical documentation, as cited in the manuscript}, year = {2024}
}
@misc{meta2024,
  author = {{Meta Platforms}}, title = {Technical documentation, as cited in the manuscript}, year = {2024}
}
@misc{mckinsey2024,
  author = {{McKinsey}}, title = {Report, as cited in the manuscript}, year = {2024}
}
@misc{mckinseygi2024,
  author = {{McKinsey Global Institute}}, title = {Report, as cited in the manuscript}, year = {2024}
}
@misc{idc2024,
  author = {{IDC}}, title = {Report, as cited in the manuscript}, year = {2024}
}
@misc{epochai2024,
  author = {{Epoch AI}}, title = {Report, as cited in the manuscript}, year = {2024}
}
@misc{stanfordhai2024,
  author = {{Stanford HAI}}, title = {AI Index Report}, year = {2024}
}
@misc{tsmc2024,
  author = {{TSMC}}, title = {Technology Report, as cited in the manuscript}, year = {2024}
}
@misc{synergy2024,
  author = {{Synergy Research Group}}, title = {Report, as cited in the manuscript}, year = {2024}
}
@misc{qsrankings2024,
  author = {{QS Rankings}}, title = {As cited in the manuscript}, year = {2024}
}
@misc{techcouncilau2024,
  author = {{Tech Council of Australia}}, title = {Report, as cited in the manuscript}, year = {2024}
}
@misc{ausaiethics2024,
  author = {{Australian Government}}, title = {Australia's AI Ethics Framework (revision)}, year = {2024}
}
@misc{cisco2024,
  author = {{Cisco}}, title = {Smart+Connected Communities, as cited in the manuscript}, year = {2024}
}
@misc{govtechsg2024,
  author = {{GovTech Singapore}}, title = {As cited in the manuscript}, year = {2024}
}
@misc{khanacademy2024,
  author = {{Khan Academy}}, title = {As cited in the manuscript}, year = {2024}
}
@misc{mitmedialab2023,
  author = {{MIT Media Lab}}, title = {As cited in the manuscript}, year = {2023}
}
@misc{stanfordvhil2023,
  author = {{Stanford Virtual Human Interaction Lab}}, title = {As cited in the manuscript}, year = {2023}
}
@misc{idrcunesco2023,
  author = {{IDRC/UNESCO}}, title = {As cited in the manuscript}, year = {2023}
}
@misc{cacc2023,
  author = {{CACC}}, title = {As cited in the manuscript, August}, year = {2023}
}
@misc{embrapainpe2023,
  author = {{Embrapa/INPE}}, title = {As cited in the manuscript}, year = {2023}
}
@misc{conab2024,
  author = {{CONAB}}, title = {As cited in the manuscript}, year = {2024}
}
@misc{gsma2024,
  author = {{GSMA}}, title = {Mobile Economy Sub-Saharan Africa}, year = {2024}
}
@misc{tomtom2023,
  author = {{TomTom}}, title = {Traffic Index}, year = {2023}
}
@misc{riotinto2023,
  author = {{Rio Tinto}}, title = {Annual Report}, year = {2023}
}
@misc{sber2023,
  author = {{Sber}}, title = {Annual Report}, year = {2023}
}
@misc{iiss2024,
  author = {{IISS}}, title = {The Military Balance}, year = {2024}
}
@misc{unity2023,
  author = {{Unity Technologies}}, title = {As cited in the manuscript}, year = {2023}
}
@misc{cma2026,
  author = {{China Meteorological Administration}}, title = {MAZU early-warning platform documentation}, year = {2026}
}
@misc{chinamem2026,
  author = {{Ministerio de Gesti{\'o}n de Emergencias de China}}, title = {As cited in the manuscript}, year = {2026}
}
@misc{ecns2026,
  author = {{ECNS}}, title = {News report, as cited in the manuscript, July}, year = {2026}
}
@misc{globaltimes2026,
  author = {{Global Times}}, title = {News report, as cited in the manuscript, July}, year = {2026}
}
@misc{scmp2026,
  author = {{South China Morning Post}}, title = {News report, as cited in the manuscript, July}, year = {2026}
}
@misc{pipl2021,
  author = {{China}}, title = {Personal Information Protection Law (PIPL)}, year = {2021}
}
@misc{privacyact1988,
  author = {{Australia}}, title = {Privacy Act 1988}, year = {1988}
}
@misc{gdpr2016,
  author = {{Uni{\'o}n Europea}}, title = {Reglamento General de Protecci{\'o}n de Datos (GDPR)}, year = {2016}
}
@misc{aiact2024,
  author = {{Uni{\'o}n Europea}}, title = {Reglamento de Inteligencia Artificial (EU AI Act)}, year = {2024}
}
@misc{airmf2023,
  author = {{NIST}}, title = {AI Risk Management Framework 1.0}, year = {2023}
}
@misc{a2a2024,
  author = {{Google DeepMind}}, title = {Agent2Agent (A2A) Protocol}, year = {2024}
}
"""
