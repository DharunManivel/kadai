# Install the required libraries
!pip install googlemaps
!pip install googletrans==4.0.0rc1

import re
import json
import time
import googlemaps
from googletrans import Translator

# Initialize translator (optional)
translator = Translator()

# Your Google API key
API_KEY = "GOOGLE_KEY"  # Replace with your API key
gmaps = googlemaps.Client(key=API_KEY)

# Provided Tamil text; 
tamil_text = """
நியூ சன்ரைஸ், கள்ளக்குறிச்சி பேருந்து நிலையம், விழுப்புரம். Special : பாப்கார்ன்

குணா சுக்குகாபி, மானாம்பதி, திருப்போரூர். Special : சுக்குகாபி

பசும்பால் பஞ்சாமி அய்யர் கடை, கும்பகோணம். Special : காபி

முராரி ஸ்வீட், கும்பகோணம். Special : பூரி, பாஸந்தி, ட்ரை ஜாமூன்களுக்கும் பிரபலமான கடை(மயிலாடுதுறை மற்றும் திருவாரூரிலும் கிளைகள் உண்டு)

ஸ்ரீ கிருஷ்ணா ஹோட்டல், வடவள்ளி, கோவை. Special : மட்டன் குழம்பு, தந்தூரி சிக்கன்

ஹோட்டல் உஷா ராணி, இளம்பிள்ளை, வேம்படிதாளம், சேலம். Special : மூளை வறுவல், நாட்டு கோழி பெப்பர் வறுவல், மட்டன் சுக்கா

மயில் மார்க் மிட்டாய் கடை, திருச்சி, திருச்சி ரயில்வே ஸ்டேஷன் எதிரே. Special : முந்திரி அல்வா, முந்திரி பக்கோடா

ராஜூ ஆம்லேட், பரோடா ஓல்ட் பத்ரா ரோடு. Special : ஆம்லேட்

ஷஹ்ரன் ஹோட்டல், ஹைதராபாத் சார்மினார் கோபுரம். Special : லஸ்ஸி பலூடா

முதலியார் கடை, மதுரை தேவர் சிலை அருகே, மதுரை கோரிப்பாளையம் பஸ் ஸ்டாப். Special : முட்டை இட்லி

R.ரெங்கநாதன் கரம் கடை(செட்டி கடை), ஜவஹர் பஜார் கருப்பாயி கோவிலுக்கு சிறிது முன்பு, கரூர். Special : சீம் பால் கட்டி

AJJ மஸ்கோத் அல்வா, முதலூர், தூத்துக்குடி. Special : மஸ்கோத் அல்வா

காளத்தி கடை கிழக்கு மாட வீதி, மைலாபூர். Special : ரோஸ் மில்க்

கந்தன் தட்டு வடை செட், சேலம் பஜார் தெரு Special : தட்டு வடை செட்.

கௌரி மெஸ், ராம் நகர், கோவை. Special : சிக்கன் கிரேவி, பூ மீன்

'மங்களாம்பிகா' இட்லி, கும்பகோணம். Special : மிளகாய்ப் பொடி, இட்லி

JB சவுத்திரி பாதாம் பால் கடை, மேற்கு மாசி வீதி, மதுரை. Special : பாதாம் பால்

விருத்தாசலம். Special : தவலை வடை !!

ஆறுமுகம் பரோட்டா ஸ்டால், மதுரை அழகர் கோவில் ரோடு, தல்லாகுலம். Special : பரோட்டா

112 இலக்கம், மதுரை காமராஜர் சாலை, பழைய குயவர் பாளையம் சாலை, அழகர்கோவில். Special : தோசை

NNK மற்றும் NNR, அம்மாபேட்டை, சேலம் TVK ரோட்டில். Special : எசென்ஸ் தோசை

திண்டுக்கல் சிவா பிரியாணி, வேணு பிரியாணி இருக்கும் அதே தெரு. Special : மிளகு கொழம்பு

ஆதிகுடி ரவா பொங்கல், தேவர் ஹால் பஸ் ஸ்டாப், திருச்சி மெயின் கார்ட் கேட், கெயிட்டி, திருச்சி. Special : ரவா பொங்கல்

மௌலானா பேக்கரி, கூத்தாநல்லூர். Special : தம்ரூட்

உடுப்பி கிருஷ்ண விலாஸ், சிதம்பரம். Special : கத்திரிக்காய் கொத்சு

ஸ்ரீ சரஸ்வதி டீ ஸ்டால், ராமசேரி, கோயம்பத்தூர். Special : இட்லி

SRR கபே, திருவாரூர் பேருந்து நிலையம். Special : கலவை சாதங்கள்

வாசன், திருவாரூர். Special : பாதாம்அல்வா

உடுப்பி கிருஷ்ணா போளி ஸ்டால், 17, டான்சி நகர் , இரண்டாவது தெரு, தரமணி லிங்க் ரோடு , வேளச்சேரி. Special : போளி, மற்றும் இனிப்பு வகைகள்.

A -1 ஹோட்டல், பெருமாள்புரம் ரவுண்டானா அருகில், திருநெல்வேலி. Special : சிக்கன் 65, மஜ்ரா சிக்கன், ஜிஞ்சர் சிக்கன்

வசந்த பவன், பேருந்து நிலையம் அருகில், திருநெல்வேலி. Special : மதிய உணவு மற்றும் பரோட்டா

PLA கிருஷ்ணா இன், திருச்சி மத்திய பேருந்து நிலையம் அருகில். Special : பாயசம் மற்றும் அப்பளம்

தேவர் ஹோட்டல், ராஜப்பா நகர், மெடிக்கல் காலேஜ் ரோடு, தஞ்சாவூர். Special : பருப்பு உருண்டை குழம்பு

அவ்வா இட்லி கடை, பூ மார்க்கெட், செளடேஸ்வரி கோவில் பின்புறம், கோவை. Special : இட்லி

வளர்மதி மெஸ், ரேஸ்கோர்ஸ், கோவை. Special : பிச்சிப்போட்ட கோழி, நெத்திலி மீன் ஃப்ரை

ஸ்ரீகெளரி மெஸ், ராம் நகர், காந்திபுரம், கோவை. Special : கட்லா மீனும், சிக்கன் கிரேவியும்

கண்ணன்ணன் விருந்து, RS புரம் TV சாமி ரோடு புடிச்சு மேட்டுப்பாளையம் ரோடு நோக்கி. Special : குடல் கூட்டு, மட்டன் சாப்ஸ், நாட்டுக் கோழி வறுவல்..

டோபாஸ் ஐயர் மெஸ், பேரூர், கோவை. Special : ஊத்தாப்பம், ஆனியன் ரோஸ்ட், மசால் ரோஸ்ட்

சத்யா மெஸ், புற்றுக்கண் மாரியம்மன் கோயில் அருகே, பாப்பநாயக்கன் பாளையம், கோவை. Special : கம்பு தோசை, சோள தோசை, ராகி தோசை, கோதுமை தோசை

வைரவிழா பள்ளி அருகில் உள்ள பாய் கடை. Special : காரப்பொறி

ஜெர்மன் ஹோட்டல், காரணம்பேட்டை, சூலூர். Special : நாட்டுக் கோழி வறுவல், கிள்ளி போடப்பட்ட வரமிளகாயுடன் செம காரத்துடன் பட்டர் நானு

மதுரை அம்மா மெஸ், பவர் ஹவுஸ் ரோடு, கோவை. Special : சாப்பாடு

படையப்பா மெஸ், குமரன் சாலை, திருப்பூர். Special : முயல் கறி ஸ்பெசல்

இந்தியன் பஞ்சாபி தாபா, சித்தோடு, ஈரோடு. Special : பள்ளிபாளையம் சிக்கன், நாட்டுக்கோழி, பாயாசத்தில் சேமியாவும், முந்திரியும்

தாஸ் லாட்ஜ் கேண்டீன், நஞ்சப்பா ரோடு, உப்பிலிபாளையம், கோவை. Special : பரோட்டா

மாரிமுத்து போண்டா கடை, முருகாலயா தியேட்டர் நேர் எதிரே, பொள்ளாச்சி. Special : போண்டா பஜ்ஜி

அபூர்வ விலாஸ், கணபதி, கோவை. Special : தேங்காய் பால், பலகாரம் ஸ்பெசல்

ரமேஷ் மெஸ், அழகேசன் சாலை, சாய்பாபா காலணி, கோவை. Special : ஆப்பம், தேங்காய் சட்னி

கடுக்கன் விலாஸ், வஉசி பூங்கா அருகில், ஈரோடு. Special : கம்மங்கூழ், ராகிக் கூழ், தயிர் வடை, மசால மோர்

ஓம்சக்தி ஹோட்டல், இடையர் வீதி அருகே உள்ள குரும்பூர் சந்து, மநக வீதி, கோவை. Special : சிக்கன் 65

திருமூர்த்தி டீ & டிபன் ஸ்டால், அவிநாசி. Special : தோசை, ஆப்பம்

ரயிலடி சுப்பையா மெஸ், தஞ்சை. Special : ஏழு வகை சட்னியுடன் சுவை மிக்க இரவு சிற்றுண்டி

பாரதியார் உணவகம், வரதராஜா மில் அருகில், பீளமேடு. Special : திண்டுக்கல் ரோஸ்ட், மற்றும் கோதுமை தோசை

பிங்க்பெர்ரி, 100 ஃபீட் ரோடு, தூபன்ஹள்ளி, இந்திரா நகர், பெங்களூர். Special : தயிர்கிரீம்

குணங்குடிதாசன் சர்பத், கீழவாசல், தஞ்சாவூர். Special : பால் சர்பத்

Jannal Kadai, மயிலாப்பூர் கற்பகாம்பாள் கோவில் இடதுபுறம் சந்தில், சென்னை. Special : Bajji

கௌரி சங்கர் ரசவடை, வடசேரி, நாகர்கோவில். Special : ரசவடை

ஆதிகாலத்து ஒரிஜினல் நெய் மிட்டாய் கடை, மதுரை. Special : கிழங்கு பொட்டலம்

A.V.K மீன் சாப்பாட்டு கடை, ஆர்காட் ரோடு, L.V பிரசாத் ரோடு. Special : மீன் சாப்பாட்டு

குஞ்சான் செட்டி கடை, மன்னார்குடி. Special : காராபூந்தி, மைசூர்பாக்.

டெல்லி ஸ்வீட்ஸ், மன்னார்குடி. Special : முந்திரி அல்வா

ரோஜா மார்க் இனிப்புகள், கும்பகோணம். Special : ஸ்பெஷல் கமர்கட், பொரி உருண்டை, கடலை உருண்டை

ரத்னா கபே, திருவல்லிக்கேணி. Special : சாம்பார்

சங்கர விலாஸ், கீழ ஆண்டார் வீதி, திருச்சி. Special : பூரி, கடப்பா

தஞ்சாவூர் மெஸ், மேற்கு மாம்பலம், சென்னை. Special : பூரி,கடப்பா

பார்த்தசாரதி விலாஸ், மேலவிபூதி பிரகாரம், திருவானைக்கா கோயில். Special : நெய் தோசை

சொசைட்டி பால்கோவா, மணப்பாறை. Special : பால்கோவா

இத்தாலியன் பேக்கரி, கும்பகோணம், தஞ்சை அய்யம்பேட்டை. Special : டீ, காபி, பிஸ்கட்

கோபு ஐயங்கார் கடை, மதுரை, மீனாக்ஷி அம்மன் கோவில். Special : சீவல் தோசை

காபி பேலஸ், எல்லையம்மன் கோயில் தெரு, தஞ்சாவூர். Special : டீ, காபி.

ராவ்ஜி தள்ளுவண்டி பிரியாணி கடை, திருச்சி பெரிய கடைவீதி. Special : பிரியாணி

காவேரி ஜூஸ் கடை, 5 கார்னர், கோவை. Special : நன்னாரி சர்பத், ரோஸ் மில்க்

பிரியா, கோவை சித்தாப்புதூர் அய்யப்பன் கோவில். Special : அடப்பிரதமன்

சிவ விலாஸ் ஹோட்டல், கோவை, கணபதி. Special : தேங்காய் பால்

மயூரா பேக்கரி, கருமத்தம்பட்டி மெயின் ஜங்ஷன். Special : காரட் கேக்

பழனியம்மா பாட்டி டீக்கடை, சரவணம்பட்டி, கோவை. Special : இஞ்சி டீ

கணபதி மெஸ், வடவள்ளி பழமுதிர் நிலையம் அருகே, கோவை. Special : ஈவ்னிங் வெஜிடேரியன் டிபன்.

பர்மா பாய் கடை, கோவை. Special : பரோட்டா பெப்பர் லெக்

எஸ்.ஆர்.கே.பி மெஸ், ஹோப் காலேஜ், கோவை. Special : ஃபுல் மீல்ஸ்

ஸ்ரீசாய் கபே, கோவை அண்ணா சிலை. Special : ஃபுல் மீல்ஸ்

Barbeque Nation, கோவை டவுன் ஹால். Special : Unlimited Barbeque

மீசை பாணி பூரி, சுக்ரவார்பேட்டை. Special : முட்டை பூரி

கொங்கு மெஸ், ஹோப் காலேஜ், கோவை. Special : ஃபுல் மீல்ஸ்

பாபு ஹோட்டல், கோவை சுந்தராபுரம் பஸ்ஸ்டாப். Special : ஆப்பம், சாம்பார் பொடி

SMS ஹோட்டல், கோவை, Special : நல்லி எலும்பு சூப், மட்டன் கீமா, தோசை

கீர்த்தி மெஸ், தெற்கு ஆர்.டி.ஓ ஆபீஸ், கோவை. Special : ஃபுல் மீல்ஸ்

அன்ன பூரணி மெஸ், காந்திபுரம் வீதி 1, கோவை. Special : அனைத்து வகை சிற்றுண்டி

ஆஜ்மர் பிரியாணி, மணி கூண்டு, கோவை. Special : பிரியாணி, குஸ்கா

MR ஹோட்டல், கோவை நேரு ஸ்டேடியம். Special : நாட்டுக் கோழி லெக் பீஸ் ப்ரை

CFC HOT FRIED CHICKEN, கோவை ராம்நகர் சிட்டி டவர் ஹோட்டலில். Special : வறுத்த கோழி

நல்உணவு, கோவை ஆர்எஸ் புரம் அன்னபூர்ணா அருகில். Special : சிறு தானியங்கள் உணவு

பிரியாணி மண்டி, ராம்நகர் காளிங்கராயர் தெரு. Special : பிரியாணி

ஹாஜி முத்து ராவுத்தர் பிரியாணி, உக்கடம், கோவை. Special : பிரியாணி, அரி பத்திரி

லக்ஷ்மி சங்கர் மெஸ், ஜி சி டி, கோவை. Special : ஃபுல் மீல்ஸ், எண்ணையில்லா சாப்பாடு

ஆச்சி மெஸ், லாரி பேட்டை, கோவை. Special : 12 வகை வெரைட்டி சாத வகைகள்

சஹாய் க்ரில்ஸ், கோவை, பீளமேடு. Special : செட்டிநாடு க்ரில், பெப்பர் க்ரில்

ஸ்ரீ லக்ஷ்மி நாராயண டீ காஃபீ, வரதராஜபுரம், கோவை. Special : குருமா, பரோட்டா

கோவை RS புரம் பாலாஜி மெஸ், பெண்களே சமையல். Special : மீன் குழும்பு, கைமா வடை

அம்மா மெஸ், லாரி பேட்டை, கோவை. Special : மீன் குழம்பு, மீன் சாப்பாடு

குப்பண்ணா ஹோட்டல், கோயம்புத்தூர், ராம்நகர். Special : அசைவ சாப்பாடு

சி கே மீல்ஸ், ரயில் நிலயம், கோவை. Special : அளவுச் சாப்பாடு

வில்லேஜ் லஞ்ச் ஹோட்டல், கோவை ரெக்ஸ் ஆஸ்பத்திரி. Special : அனைத்து வித தோசைகள்

பாரதி மெஸ், NEAR NATIONAL MODEL SCHOOL, கோவை. Special : அனைத்து வித தோசைகள்

கீதா கெண்டீன், ரயில் நிலையம், கோவை. Special : அனைத்து வகை டிபன்

கண்ணணண் கறி விருந்து, கோவை. Special : நாட்டுக் கோழி சிக்கன், புதினா சிக்கன்

சுப்பு மெஸ், ரயில் நிலையம், கோவை. Special : சைவ, அசைவ ஃபுல் மீல்ஸ்

ஃபுட் கார்டன், RS Puram, கோவை. Special : தயிர் பூரி

குப்தா ஜி சாட்ஸ், கோவை சாய்பாபா காலனி, சர்ச் ரோடு. Special : தயிர் பூரி

வைரமாளிகை, நெல்லை. Special : ப்ரைடு சிக்கன், ஷார்ஜா மில்க்‌ஷேக்

உமர்கையாம், லலிதா ஜுவல்லரி, தி.நகர். Special : எண்ணெய் கத்தரிக்காய், தாள்ச்சா முஸ்லீம் வீட்டு பிரியாணி

மாமு கார்டன் ஹோட்டல், பரமக்குடி. Special : சைனீஸ் உணவு

சுகுணவிலாஸ் ஹோட்டல், அண்ணா சிலை, கடை வீதி, திருசெங்கோடு. Special : பள்ளிபாளையம் சிக்கன்

சீனியப்பா ஹோட்டல், கீழக்கரை. Special : பரோட்டா, சால்னா

ஜெய் சக்தி சைவ ஹோட்டல், கோவில்பட்டி. Special : நிறைய மிளகு போட்டு CHETTINAADU சூப்

ஃப்ளெமிங்கோ ஹோட்டல், வேளச்சேரி 100 அடி பை பாஸ் ரோடு. Special : சாப்பாடு

மாயாபஜார், சேலம். Special : நான்வெஜ் ஹோட்டல்,

மாமன் பிரியாணி, ஈரோடு பன்னீர் செல்வம் பார்க். Special : பிரியாணி

அன்னை மெஸ், குன்னத்தூர் பஸ் ஸ்டாண்ட். Special : நாட்டுக் கோழிக் குழம்பு, ஆசாரி வறுவல்.

செந்தில் மெஸ், யானைமலை, ஒத்தக்கடை. Special : மதுரை மட்டன் சுக்கா

மீனாட்சி மெஸ், யானைமலை, ஒத்தக்கடை. Special : மதுரை மட்டன் சுக்கா

கதிர்வேல் வாத்துக்கடை, வேலூர் பரமத்தி. Special : வாத்துமுட்டை ஆம்லெட்

பார்டர் ரஹ்மத் புரோட்டாக்கடை, தென்காசி. Special : பெப்பர்சிக்கன், பெப்பர்காடை

பொன்னுசாமி ஹோட்டல், ராயபேட்டை. Special : நெத்திலி ப்ரை, சிக்கன் லாலிபாப்

தூத்துக்குடி பரோட்டோ கடை, கோவை ஹோப்ஸ். Special : பரோட்டோ

தோசா கார்னர், சேலம் அத்வைத் ஆஸ்ரமம் ரோடு. Special : அனைத்து வித தோசைகள்

செல்வம் ஹோட்டல், சேலம் அப்சரா மேடு. Special : பரோட்டா சால்னா

ராணி டிபன் ஸ்டால், கரூர். Special : கொத்து பரோட்டா

தேவர் மெஸ், சுங்கராம வீதி, பாரீஸ். Special : பரோட்டா குருமா:

மாருதி ஹோட்டல், சுசீந்திரம். Special : ஃபுல் மீல்ஸ்

டைமண்ட் டீ ஸ்டால், பழனி பஸ் ஸ்டாண்ட். Special : டீ

ராயல் புரோட்டாஸ், கரூர்-பள்ளபட்டி. Special : அனைத்து வித புரோட்டா

ஹோட்டல் சத்தார்ஸ், தஞ்சாவூர். Special : பிரியாணி

சென்ட்ரல் பிரியாணி கடை, திருப்பூர் காங்கேயம் கிராஸ் ரோடு. Special : பிரியாணி

ஜோஸ் கடல் மீன் உணவகம், குமார் நகர், திருப்பூர். Special : கடல் மீன் உணவு

ஆச்சிஸ், திண்டுக்கல். Special : அயிரை மீன் பக்கோடா

செல்லம்மாள் மண்பானை உணவகம், திருச்சி புத்தூர் திரவுபதி அம்மன் கோவில் எதிரில். Special : ஃபுல் மீல்ஸ்

முத்துபிள்ளை கேண்டின், புதுக்கோட்டை. Special : பரோட்டா 4 வகை சால்னா

தீன், தஞ்சாவூர். Special : சிக்கன் முர்தாபா

சார்மினார், ராயப்பேட்டை. Special : தந்தூரி சிக்கன்

கணேஷ் மெஸ், ஆண்டிபட்டி. Special : பூசணிப் பொரியல்

ஆனந்தாஸ் ஹோட்டல், ராஜபாளையம். Special : ஃபுல் மீல்ஸ்

சலாமத் ஹோட்டல், அண்ணாசாலை, சென்னை. Special : சுக்கா பரோட்டா

தங்கையா ஸ்வீட் ஸ்டால், திசையன்விளை. Special : மஸ்கோத் அல்வா

ஶ்ரீ சாய் உயர் தர சைவ உணவகம், தஞ்சாவூர் மெயின் ரோடு, திருச்சி. Special : ஆனியன் ஊத்தப்பம்

கதிரவன் ஹோட்டல், ஸ்ரீவில்லிப்புத்தூர். Special : காபி

ஆள் ரீம், திருவல்லிக்கேணி. Special : பிரியாணி

தாஸ் ஜிகர்தண்டா, பெரியகுளம் ரோடு, தேனி பழைய பஸ்ஸ்டாண்ட். Special : ஜிகர்தண்டா

டேன்ஜரின் ரெஸ்டாரன்ட், ரேஸ்கோர்ஸ், கோவை. Special : சாப்பாடு

சாய் கப்சப், RS PURAM, கோவை. Special : இஞ்சி டீ:

இளநீர் சர்பத் கடை, பெல் ஹோட்டல் எதிரில், மதுரை தமிழ்ச்சங்கம் ரோடு. Special : இளநீர் சர்பத்

ஸ்ரீ விநாயக ஸ்வீட் காரம், குருக்கத்தி. Special : எள்ளுருண்டை

அரசன் மெஸ் மண்பானை சமையல், திருநெல்வேலி, மதுரை பைபாஸ் சாலை. Special : அன் லிமிட்டட் சாப்பாடு

ஸ்ரீ கிருஷ்ணபவன், கும்பகோணம் ரயில் நிலையம் வெளியேறும் பாதை. Special : அனைத்து வித தோசைகள்

நாயர் மெஸ், திருவல்லிக்கேணி. Special : மட்டன் குழம்பு வஞ்சிரம் வறுவல்

ஆந்திரா கரீ ஹோட்டல், தங்க ரீகல் தியேட்டர், மதுரை. Special : தட்டு இட்லி

அழகப்பா செட்டிநாடு மெஸ், GST மெயின்ரோடு, சானடோரியம், சென்னை. Special : குஸ்கா

அழகி பிரியாணி ஹோட்டல், ஒக்கேனக்கல் மெயின் ரோடு. Special : அன்லிமிடட் பிரியாணி

பழநியப்பா மெஸ், புதுக்கோட்டை. Special : பஃப் பரோட்டோ

ஜானகிராமன் சைவ உணவகம், திருநெல்வேலி பெரியார் பேருந்து நிலையம் அருகே. Special : அனைத்து வித தோசைகள்

Jacob's Kitchen, காதர் நவாஸ் கான் ரோடு, கானாடுகாத்தான். Special : உப்புகறி, மண்பானை மீன் குழம்பு

பிரேமா மெஸ், தூத்துக்குடி பழைய பஸ்ஸ்டாண்ட். Special : கானத்துவையல், எள்ளுத்துவையல்

அண்ணாமலை சைவ ஹோட்டல், நெல்லை காந்திமதி கோவில். Special : மதிய சாப்பாடு, பிரண்டை துவையல்

அஜித் மீன் ஹோட்டல், நாகர்கோவில். Special : ஃபுல் மீன் மீல்ஸ்

அக்பர் மெஸ், பெரியமேடு. Special : மட்டன் பிரியாணி

வெங்கடேஷ்வரா ஹோட்டல், அப்பத்தூர். Special : சமோசா

பரமக்குடி பரோட்டா, பரமக்குடி பஸ் ஸ்டான்ட் எதிரில். Special : சால்னா

JMS சர்பத் கடை, திண்டுக்கல். Special : சர்பத்

ஸ்ரீ பாலாஜி பவன் ஹைகிளாஸ் வெஜ ஹோட்டல், திண்டுக்கல். Special : ஃபுல் வெஜ் மீல்ஸ்

சார்லஸ் ஹோட்டல், மதுர நரிமேடு அரசன் சுவீட்ஸ் அருகில். Special : பரோட்டா, 3 கூட்டு சால்னா

பைவ் ஸ்டார் இரவு ஹோட்டல், சின்னசேலம். Special : தோசை, நாலு வகை சட்னி

மொஹைதீன் பிரியாணி, பல்லாவரம். Special : பிரியாணி

போஜன், சூளைமேடு சிக்னல். Special : சோலா பூரி

ரிலாக்ஸ் காபி பார், திண்டுக்கல். Special : வடை, குருமா

பட்ஸ் ஹோட்டல் டீ, தாம்பரம் பஸ்டாண்ட் உள்ளே. Special : Tea

ஹரிஷ் பேக்கரி உப்பு ரொட்டி, நாகூர். Special : உப்புரொட்டி, தம்ரூட்

சபரீஷ் ஹோட்டல், மதுரை சென்னை சில்க்ஸ் அருகே. Special : ஹைதரபாத் பிரியாணி :

கேரளா மெஸ், திருச்சி அஹ்மத் பிரதர்ஸ்கு பக்கத்து சந்து. Special : பரோட்டா வித் சில்லி

காந்தி கடை சால்னா, பரமக்குடி. Special : பரோட்டா

குறிஞ்சி ஹோட்டல், இராம்நாட். Special : பரோட்டா, நெய் மீன் கறி

அப்பா மெஸ், திருப்பூர் கரட்டாங்காடு பஸ் ஸ்டாப். Special : ஃபுல் மீல்ஸ்

மணி கவுண்டர் மெஸ், திருப்பூர் குமார் நகர் 60 அடி ரோடு. Special : சிந்தாமணி சிக்கன்

அல் ரீம் ஹோட்டல், திருவல்லிக்கணி. Special : ஸ்பெசல் பிரியாணி, ப்ரைடு ரைஸ்

புளியமரத்துக்கடை, ஶ்ரீவில்லிபுத்தூர். Special : ஸ்பெஷல் பால்கோவா

ஸ்ரீ அன்பு பவன், கோபி பஸ் நிலையம், கோபி. Special : ஃபுல் மீல்ஸ்

தனசேகர் சிக்கன் சென்டர், முத்துநாயக்கன்பட்டி. Special : சிக்கன்

தம்புடு ஹோட்டல், பல்லடம் போலிஸ் ஸ்டேசன். Special : இரவு இட்லி, ரோஸ்ட், பரோட்டா

செட்டியார் கடை, திருப்பூர். Special : டயனமைட் சிக்கன் :

Aachi Chetinad Hotel ஹோட்டல், ஈரோடு டெலிபோன் எக்ஸ்‌சேன்ஜ். Special : மூளை பிரட்டல்

BL ரெஸ்டாரன்ட், கரூர். Special : காரசட்னி இட்லி :

கண்ணன் ஹோட்டல், மதுரை புதூர் சர்ச். Special : மூளை ஃப்ரை

அம்மன் மெஸ், கோபிச்செட்டிபாளையம் சீதாலட்சுமி மண்டபம் அருகில். Special : சைவம் அசைவம் உணவு

சுதா மெஸ், குமாரபாளையம். Special : அசைவம் வீட்டு சாப்பாடு :

பத்மா மெஸ், விழுப்புரம் கலெக்டர் ஆஃபீஸ் அருகில். Special : அனைத்து வித தோசைகள், ஃபுல் மீல்ஸ்

சுல்தான் பிரியாணி, சங்கரன்கோவில். Special : பிரியாணி

கரம் மது கரம் ஸ்டால், கரூர் சுபாஷ் சந்திரபோஸ் சிலை அருகில், கரூர். Special : Sweets

ராமசாமி மட்டன், திருப்பூர் புதிய பஸ்நிலையம், திருப்பூர். Special : மட்டன், குடல்பிஃரை

சிவா சில்லி, கரூர் செங்குந்தபுரம். Special : மீன், சில்லி சிக்கன், பிரியாணி

மிட்நைட் மசாலா ஹோட்டல், கோடம்பாக்கம். Special : லஞ்ச், டின்னெர்.

சுப்பையா இட்லி கடை, தஞ்சாவூர் JUNCTION. Special : இட்லி

கோபால்நாயுடு ஹோட்டல், இளம்பிள்ளை. Special : ஃபுல் மீல்ஸ்

ராவியத் ஸ்வீட் பேலஸ், வள்ளல் சீதக்காதிரோடு, கீழக்கரை. Special : ஸ்பெஷல் தொதல்

கற்பகம் ஹோட்டல், திருச்சி தேவர்ஹால் எதிர்புறம். Special : இட்லி, தோசை, சாம்பார்

ஸ்ரீபிரியா மெஸ், காரைக்குடி. Special : நாட்டுக் கோழி கிரேவி

ஹோட்டல் ராமன், சீர்காழி புத்தூர் சாலை. Special : மீன் வறுவல், இறா வறுவல்

வீட்டு இட்லி, மதுரை அலங்கார் தியேட்டர் அருகில். Special : வீட்டு இட்லி, ஃபுல் மீல்ஸ்

ஹோட்டல் அர்ச்சனா, மதுரை. Special : நண்டு தோசை :

கவுண்டர் மெஸ், அவினாசி ஆட்டயாம்பாளையம். Special : அசைவச் சாப்பாடு

முத்துமெஸ், தாராபுரம் ரோடு, திருப்பூர். Special : அசைவ சாப்பாடு

செல்லமணி டிபன் கடை, தேனி. Special : 5 வகை சட்னி, பணியாரம்

செல்வம் கூல் ட்ரிங்க்ஸ், சிவகிரி. Special : ஐஸ்கிரீம்

அ1 மெஸ், கோவில்பட்டி. Special : அசைவ சாப்பாடு

இந்திராணி அக்கா இட்லி கடை, காரணம் பேட்டை. Special : இட்லி

திருப்பூர் ஷெரிப் காலனி மெயின்ரோடு. Special : அடை சுண்டல்

மாரீஸ் ரெஸ்டாரண்ட், இரத்தினமங்கலம், வண்டலுர் டூ கேளம்பாக்கம் ரோடு. Special : :ஃபுல் மீல்ஸ்

கண்ணன் ஹோட்டல், திருச்சி மத்திய பேருந்து நிலையம். Special : பாதம் பால்

தென்பனை, உளுந்தூர்பேட்டை. Special : இயற்கைமுறை குளிர்பானக் கடை

ராணி விலாஸ், செக்கானூரனி. Special : குடல் குழம்பு, குழி ஆம்லெட், ரத்த பொரியல்

வீட்டுச் சாப்பாடு, அய்யம்பேட்டை தாண்டி 15-2 கிமி, தஞ்சை – கும்பகோணம். Special : வீட்டுச் சாப்பாடு

ரோட்டு கடை, சென்னை ஓட்டேரி தாதாஷாமக்கான் பகுதி. Special : சுக்கா கபாப், வடை கபாப், வடை வறுவல்

சேகர் கடை இட்லி, மராட்டியர் அரண்மனை அருகில், தஞ்சை. Special : இட்லி

பெங்களூர் AL BAK பிரியாணி, மல்லேஸ்வரம், ராஜாஜிநகர். Special : பிரியாணி

பாலன் உணவகம், கேணிக்கரை சந்திப்பு, இராமநாதபுரம். Special : விதம் விதமான தோசை

ஹோட்டல் சுவை, திருச்சி சத்திரம் பஸ்ஸ்டாண்ட். Special : இட்லி, தோசை, பொங்கல் வடை, காபி

பார்டர் கடை, செங்கோட்டை. Special : பிரைடு சிக்கன்

அய்யரக்கா கடை, செங்கோட்டை. Special : தயிர்வடை

கொங்கு மீன் ஸ்டால், திருப்பூர் காங்கயம் ரோடு. Special : மீன் வறுவல்

HBH, ஊட்டி சேரிங் கிராஸ் அருகே. Special : பிரியாணி

இதயம் பப்ஸ், திருப்பூர் PN ரோடு, மேட்டுப்பாளையம் பஸ்டாப் அருகில். Special : வெஜ் சமோசா, அரைத்து விட்ட குருமா

ரோஷன், திருச்சி-தஞ்சாவூர் ரோடு, காட்டூர். Special : தந்தூரி

டெல்லி ஸ்வீட்ஸ், கரூர். Special : சூடான சமோசா

மதுரை ஹரிஸ் மெஸ், சின்ன சொக்கிக்குளம். Special : மணக்கும் நெய் மீன் குழம்பு

ஹோட்டல் ந்யூ இம்ரான், கொடைக்கானல். Special : மட்டன் பிரியாணி

போஜனாலாயா, மகாலக்ஷ்மி ப்ளாசா, விழுப்புரம். Special : சாப்பாடு

சங்கர் சாட், அண்ணாநகர் சரவணபவன் பின்னால். Special : தஹி, பூரி மசாலா, கட்லட், சமோசா

SK சைவ-அசைவ உணவகம், பெங்களூரு விவேக் நகர். Special : சைவ அசைவ சாப்பாடு

UFM நம்ம வீட்டு சாப்பாட்டுக் கடை, பெருந்துறை. Special : கறி சோறு

அம்மாயி வீட்டு மண் பானை சமையல், கோவை ஆவாரம்பாளையம். Special : குடல்கறி, தோசை

ஹோட்டல் விருதுநகர் செட்டிநாடு உணவகம், T-நகர். Special : சாப்பாடு

ஹோட்டல் வெல்கம், நாயுடுபுரம், கொடைக்கானல். Special : பிரியாணி

கோபு ஐயங்கார் ஓட்டல், மதுரை மீனாக்ஷி கோவில். Special : தவலை வடை

ஹோட்டல் பிரபு, நாகர்கோவில். Special : அசைவம்

ஹோட்டல் விஜயதா, நாகர்கோவில். Special : அசைவம்

ஹோட்டல் அரிஸ்டோ, கொடைக்கானல். Special : டிபன், மீல்ஸ்

காலேஜ் ஹவுஸ் லாட்ஜுக்குள் இருக்கும் ரெஸ்டாரண்ட், மதுரை. Special : சைவச் சாப்பாடு

மணி ஐயர் ஓட்டல், திருச்செந்தூர். Special : சைவச் சாப்பாடு

பாரதி மெஸ், திருவல்லிக்கேணி. Special : கேப்பைக் கூழ், முளை கட்டிய தாணியங்கள்

பஞ்சு பரோட்டா, பெருந்துறை. Special : பரோட்டா, சிக்கன் பிரியாணி

மண்சட்டி சமையல், சங்ககிரி டோல்கேட் அருகே. Special : ஃபுல் மீல்ஸ்

முருகபவன், தொப்பூர். Special : விதம் விதமான தோசை

தாஜ் ஹோட்டல், மதுரை-ராமேஸ்வரம் மெயின் ரோடு, பரமக்குடி. Special : கறிக்கஞ்சி

ஏஒன்மெஸ், கோவில்பட்டி. Special : சிக்கன் பிரியாணி, லாலிபாப், தலைக்கறி

பசுமை உணவகம், சேலையூர். Special : கருப்பட்டி காஃபி

NEW MADRAS CAFÉ, சந்தோம். Special : மாலையில் சம்சா, சாஸ்

கருப்பையா நாடார் மெஸ், சாத்தூர். Special : கரண்டி ஆம்லெட், டிங் டாங்

துளசி பிரியாணி, திண்டுக்கல். Special : நாட்டுகோழி பிரியாணி, புட்டு பரோட்டா

பார்த்தசாரதி விலாஸ், திருச்சி திருவானைக்கோவில். Special : நெய் தோசை

விஞ்சை விலாஸ், நெல்லை டவுனில் ஆர்ச் பக்கம். Special : விதம் விதமான தோசை

வெங்கடேச பவன், ஸ்ரீரங்கம் கோயில் அருகில். Special : சாம்பார் வடை, கீரை வடை

மூர்த்தி கபே, சிதம்பரம். Special : கடாய் சிக்கன்:

ஆண்டவர் அல்வா கடை, திருவையாறு. Special : அல்வா
...
"""  

# Regular expression to extract name, location, and special from each entry.
pattern = re.compile(
    r"(?P<name>[\w\s\-\.\u0B80-\u0BFF]+),\s*(?P<location>[\w\s\-\.\u0B80-\u0BFF,]+)\.\s*Special\s*:\s*(?P<special>.+)",
    re.UNICODE
)

restaurants = []

for match in pattern.finditer(tamil_text):
    name = match.group("name").strip()
    location = match.group("location").strip()
    special = match.group("special").strip()

    # Form the query: append ", Tamil Nadu" to restrict results.
    query = f"{name}, {location}, Tamil Nadu"

    # Initialize default values
    lat, lng, link = None, None, ""
    phone, rating, reviews = "", 0, 0
    candidate = None

    # --- Step 1: Use Places API for details (priority) ---
    allowed_fields = ["place_id", "rating", "user_ratings_total", "formatted_address"]
    try:
        places_result = gmaps.find_place(
            input=query,
            input_type="textquery",
            fields=allowed_fields
        )
        if places_result.get("candidates"):
            # Pick the first candidate if its address contains "Tamil Nadu"
            for cand in places_result["candidates"]:
                # Use Place Details to get formatted_address
                details = gmaps.place(place_id=cand["place_id"], fields=["formatted_address", "geometry/location", "formatted_phone_number"])
                result_details = details.get("result", {})
                formatted_address = result_details.get("formatted_address", "").lower()
                if "tamil nadu" in formatted_address:
                    candidate = cand
                    # Fetch rating and review count from the candidate
                    rating = candidate.get("rating", 0)
                    reviews = candidate.get("user_ratings_total", 0)
                    # Also fetch phone and geometry details
                    phone = result_details.get("formatted_phone_number", "")
                    location_details = result_details.get("geometry", {}).get("location", {})
                    lat = location_details.get("lat")
                    lng = location_details.get("lng")
                    break
        else:
            # If no candidate is found, try translating query to English and search again.
            translated_query = translator.translate(query, dest='en').text
            print(f"No result for '{query}'. Trying translated query: '{translated_query}'")
            places_result = gmaps.find_place(
                input=translated_query,
                input_type="textquery",
                fields=allowed_fields
            )
            if places_result.get("candidates"):
                for cand in places_result["candidates"]:
                    details = gmaps.place(place_id=cand["place_id"], fields=["formatted_address", "geometry/location", "formatted_phone_number"])
                    result_details = details.get("result", {})
                    formatted_address = result_details.get("formatted_address", "").lower()
                    if "tamil nadu" in formatted_address:
                        candidate = cand
                        rating = candidate.get("rating", 0)
                        reviews = candidate.get("user_ratings_total", 0)
                        phone = result_details.get("formatted_phone_number", "")
                        location_details = result_details.get("geometry", {}).get("location", {})
                        lat = location_details.get("lat")
                        lng = location_details.get("lng")
                        break
    except Exception as e:
        print(f"Places API error for {query}: {e}")

    # --- Step 2: Fallback: If Places API did not return coordinates, use Geocoding API ---
    if (lat is None or lng is None):
        try:
            geocode_result = gmaps.geocode(query)
            if geocode_result:
                location_data = geocode_result[0]['geometry']['location']
                lat = location_data.get('lat')
                lng = location_data.get('lng')
        except Exception as e:
            print(f"Geocode error for {query}: {e}")

    # --- Step 3: Build map link using coordinates if available ---
    if lat is not None and lng is not None:
        link = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
    else:
        link = ""

    restaurant_data = {
        "name": name,
        "location": location,
        "special": special,
        "lat": lat,
        "lng": lng,
        "phone": phone,
        "rating": rating,
        "reviews": reviews,
        "link": link
    }

    restaurants.append(restaurant_data)

    # Pause briefly to avoid rate limits

# Save the results to a JSON file with proper formatting and Unicode support
with open('restaurants-places_priority.json', 'w', encoding='utf-8') as f:
    json.dump(restaurants, f, ensure_ascii=False, indent=2)

print("Data saved to restaurants-places_priority.json")
