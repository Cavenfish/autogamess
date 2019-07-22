#Dictionary for theory levels and their input parameters
theory_dict = {'B3LYP': 'DFTTYP=B3LYP',
               'MP2': 'MPLEVL=2',
               'CCSD-T': 'CCTYP=CCSD(T)',
               'CCSD2-T': 'CCTYP=CR-CCL',
               'CCSD': 'CCTYP=CCSD',
               'BLYP': 'DFTTYP=BLYP',
               'PBE': 'DFTTYP=PBE',
               'PBE0': 'DFTTYP=PBE0',
               'M06': 'DFTTYP=M06',
               'wB97X-D': 'DFTTYP=wB97X-D',
               'M06-L': 'DFTTYP=M06-L',
               'M06-HF': 'DFTTYP=M06-HF',
               'M11': 'DFTTYP=M11',
               'M11-L': 'DFTTYP=M11-L',
               'SCS-MP2': 'MPLEVL=2',
               'MP2-SCS': 'MPLEVL=2',}

#Basis Dictionary
basis_dict = {'may-cc-pVDZ': 'may-cc-pv(d+d)z',
              'may-cc-pVTZ': 'may-cc-pv(t+d)z',
              'may-cc-pVQZ': 'may-cc-pv(q+d)z',
              'jun-cc-pVDZ': 'jun-cc-pv(d+d)z',
              'jun-cc-pVTZ': 'jun-cc-pv(t+d)z',
              'jun-cc-pVQZ': 'jun-cc-pv(q+d)z',
              'jul-cc-pVDZ': 'jul-cc-pv(d+d)z',
              'jul-cc-pVTZ': 'jul-cc-pv(t+d)z',
              'jul-cc-pVQZ': 'jul-cc-pv(q+d)z',
              'Sadlej-pVTZ': 'sadlej pvtz'}

#Molecule dictionary
molecule_dictionary ={

'H2O':['CnV 2,\n','\n',
' O           8.0  -0.0000000000   0.0000000000  -0.0123155409\n',
' H           1.0  -0.0000000000  -0.7568005555   0.5926935705\n'],

'NH3':['CnV 3,\n','\n',
' N           7.0   0.0000000000   0.0000000000   0.0000000000\n',
' H           1.0   0.0000000000   0.0000000000   0.0000000000\n'],

'CO4':['Dnd 2,\n','\n',
' C           6.0  -0.0000000000  -0.0000000000   0.0000000000\n',
' O           8.0  -0.5528609426   0.5528609426  -1.0869293833\n'],

'HCN':['CnV 4,\n','\n',
' N     7.0  -0.0000000000  -0.0000000000   0.5593351180\n',
' C     6.0   0.0000000000  -0.0000000000  -0.5650707174\n',
' H     1.0  -0.0000000000  -0.0000000000  -1.6218226179\n'],

'OCN':['CnV 4,\n','\n',
' N     7.0  -0.0000000000  -0.0000000000   0.5593351180\n',
' C     6.0   0.0000000000  -0.0000000000  -0.5650707174\n',
' O     8.0  -0.0000000000  -0.0000000000  -1.6218226179\n'],

'N2':['Dnh 4,\n','\n',
' N     7.0   0.0000000000   0.0000000000   0.5593906633\n'],

'N2O':['CnV 4,\n','\n',
' N     7.0   0.0000000000   0.0000000000   0.5099100000\n',
' N     7.0   0.0000000000   0.0000000000   1.4099100000\n',
' O     8.0   0.0000000000   0.0000000000  -0.5827700000\n'],

'N2O2':['Cnv 2,\n','\n',
' N     7.0   0.7000000000   0.0000000000   0.0000000000\n',
' O     8.0   1.2000000000   0.0000000000   0.7000000000\n'],

'N2O3':['CS\n','\n',
' N     7.0   0.5000000000   0.0000000000   0.0000000000\n',
' N     7.0  -0.5000000000   0.0000000000   0.0000000000\n',
' O     8.0   0.8000000000   0.0000000000   1.2000000000\n',
' O     8.0  -1.4000000000  -0.0000000000   0.0000000000\n'],

'N2O4':['Dnh 2,\n','\n',
' N     7.0   0.0000000000   0.0000000000   0.5116800000\n',
' O     8.0   1.0192100000   0.0000000000   1.0116800000\n'],

'N2O5':['Cnv 2,\n','\n',
' N     7.0   0.0000000000   1.0000000000   0.0000000000\n',
' O     8.0   0.0000000000   0.0000000000   0.5000000000\n',
' O     8.0   0.0000000000   1.0000000000  -1.2000000000\n',
' O     8.0   0.0000000000   2.0000000000   0.8000000000\n',],

'N3':['Dnh 4,\n','\n',
' N     7.0   0.0000000000   0.0000000000   0.8593906633\n',
' N     7.0   0.0000000000   0.0000000000   0.0000000000\n'],

'NO':['Cnv 4,\n','\n',
' N     7.0   0.0000000000   0.0000000000   0.5099100000\n',
' O     8.0   0.0000000000   0.0000000000  -0.5827700000\n'],

'NO2':['Cnv 2,\n','\n',
' N     7.0   0.0000000000   0.0000000000   0.0000000000\n',
' O     8.0   0.0000000000   1.2000000000  -0.4287700000\n'],

'NO3':['Cnv 2,\n','\n',
' N     7.0   0.0000000000   0.0000000000   0.0000000000\n',
' O     8.0   0.0000000000   1.2000000000  -0.4287700000\n',
' O     8.0   0.0000000000   0.0000000000   1.2287700000\n'],

'CO3a':['Cnv 2,\n','\n',
' C     6.0   0.0000000000   0.0000000000   0.2657450271\n',
' O     8.0  -0.7655716832   0.0000000000  -0.8165153424\n',
' O     8.0   0.0000000000   0.0000000000   1.4311936575\n'],

'CO3b':['Dnh 3,\n','\n',
' C     6.0   0.0000000000   0.0000000000   0.0000000000\n',
' O     8.0   1.2448048820   0.0000000000   0.0000000000\n'],

'CO4a':['Cnv 2,\n','\n',
' C     6.0   0.0000000000   0.0000000000   0.5491061379\n',
' O     8.0   0.0000000000   0.0000000000   1.7257804325\n',
' O     8.0   1.0168037058   0.0000000000  -0.3647926165\n',
' O     8.0   0.0000000000   0.0000000000  -1.4253013374\n'],

'CO4b':['Dnd 2,\n','\n',
' C     6.0   0.0000000000   0.0000000000   0.0000000000\n',
' O     8.0  -0.5527439913   0.5527439913  -1.0870917964\n'],

'CO5':['Cn 2,\n','\n',
' C     6.0   0.0000000000   0.0000000000  -0.8012376174\n',
' O     8.0   1.1214078621   0.0520388092  -0.0057670138\n',
' O     8.0   0.0000000000   0.0000000000  -1.9850755941\n',
' O     8.0   0.5831842521   0.4042921636   1.2971406196\n'],

'CO6a':['Dnd 2,\n','\n',
' C     6.0   0.0000000000   0.0000000000   0.0000000000\n',
' O     8.0  -0.6931030000  -0.6931030000  -0.9448310000\n',
' O     8.0   0.0000000000   0.0000000000   1.9315710000\n'],

'CO6b':['Cn 2,\n','\n',
' C     6.0   0.0000000000   0.0000000000  -0.9135839235\n',
' O     8.0   0.0000000000   0.0000000000  -2.0901547922\n',
' O     8.0   1.0662449729   0.4155539339   1.0390341517\n',
' O     8.0   1.0656136864  -0.4193249784  -0.1413572875\n',
' O     8.0   0.0000000000   0.0000000000   1.9083849874\n'],

'CO6c':['Cn 2,\n','\n',
' C     6.0   0.0000000000   0.0000000000  -0.5309621974\n',
' O     8.0   0.7656481382  -0.1056063796  -1.6402444804\n',
' O     8.0   0.0166639151   1.1294614713   0.2830409636\n',
' O     8.0   0.3963347604   0.5799588876   1.5726846155\n'],

'CO7':['Cn 2,\n','\n',
' C     6.0  -0.0000000000   0.0000000000   1.3956114033\n',
' O     8.0   0.0000000000  -0.0000000000   2.6279774303\n',
' O     8.0  -1.0866369355  -0.4198103469   0.7682622412\n',
' O     8.0  -1.3579708542   0.4182919850  -0.8166683016\n',
' O     8.0  -0.9581149314  -0.1713999012  -1.8069643563\n'],

'CO8':['C1,','\n',
' C     6.0   0.7259986955  -1.0973733945  -0.3290577298\n',
' O     8.0   1.3869757173  -2.0532020473  -0.5694030097\n',
' O     8.0  -0.0567173260  -1.1317913337   0.8273288581\n',
' O     8.0  -0.2565441214   0.0970882926   1.3802512674\n',
' O     8.0   0.7023883272   0.0071958749  -1.0481692157\n',
' O     8.0  -0.8432827905   0.5102871322  -1.3241844283\n',
' O     8.0  -1.6248862139   0.6151173485   0.8352416002\n',
' O     8.0  -1.4923316274   1.8043584646   0.5328900872\n',
' O     8.0  -0.9410756607   1.7014746628  -1.1369584294\n'],

'C2O3a':['Cnv 2,\n','\n',
' C     6.0   0.0000000000   0.7209824317   0.6810764795\n',
' O     8.0   0.0000000000   1.8493473817   1.0129786685\n',
' O     8.0   0.0000000000   0.0000000000  -0.5381102960\n'],

'C2O3b':['Cnv 2,\n','\n',
' C     6.0   0.0000000000   0.7209824317   0.6810764795\n',
' O     8.0   0.0000000000   1.8493473817   1.0129786685\n',
' O     8.0   0.0000000000   0.0000000000  -0.5381102960\n',
' C     6.0   0.0000000000   0.0000000000   1.5247396916\n'],

'C2O4a':['Cnv 2,\n','\n',
' C     6.0   0.0000000000   0.7655675120   0.5525307595\n',
' O     8.0   0.0000000000   1.6933726263   1.2750573733\n',
' O     8.0   0.0000000000   0.7472978486  -0.8275881328\n'],

'C2O4b':['Cnv 2,\n','\n',
' C     6.0   0.0000000000   0.0000000000   0.1439075810\n',
' C     6.0   0.0000000000   0.0000000000   1.4577940662\n',
' O     8.0   0.0000000000   0.0000000000  -1.8231450490\n',
' O     8.0  -1.0479112896   0.0000000000  -0.7720522817\n',
' O     8.0   0.0000000000   0.0000000000   2.6394559654\n'],

'C2O4c':['Dnh 2,\n','\n',
' C     6.0   0.0000000000   0.0000000000   0.9493708508\n',
' O     8.0   0.0000000000   1.0124121539   0.0000000000\n',
' O     8.0   0.0000000000   0.0000000000   2.1113888835\n'],

'C2O4d':['Dnh 2,\n','\n',
' C     6.0   0.0000000000   0.7386824686   0.0000000000\n',
' O     8.0   0.0000000000   1.3380281565   1.0811837700\n']}
