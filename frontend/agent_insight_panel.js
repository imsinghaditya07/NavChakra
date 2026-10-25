/**
 * Kisan Saarthi Real-Time Streaming Agent Panel (NavChakra)
 * Powered by Agent37 Streaming Engine & Grounded ICAR RAG Intelligence
 * 
 * Features:
 * - 100% Kisan Saarthi Green & White Theme
 * - Full 23 Indian Language Multilingual Support (Adapts dynamically to user-selected language)
 * - Named Kisan Saarthi (किसान सारथी)
 * - Direct real-time streaming consumption from /api/agent
 * - Speech-to-Text (Web Speech API) & Multilingual Text-to-Speech in selected language
 * - Reactive to location selection (Block/Panchayat) and language switches
 */

(function(window) {
  'use strict';

  let isStreaming = false;
  let activeAbortController = null;
  let speechRecognition = null;
  let isListening = false;

  const TTS_LANG_MAP = {
    hi: 'hi-IN', en: 'en-IN', bn: 'bn-IN', mr: 'mr-IN', te: 'te-IN',
    ta: 'ta-IN', gu: 'gu-IN', ur: 'ur-IN', kn: 'kn-IN', ml: 'ml-IN',
    or: 'or-IN', pa: 'pa-IN', as: 'as-IN', mai: 'hi-IN', sat: 'hi-IN',
    ks: 'ur-IN', ne: 'ne-NP', kok: 'mr-IN', sd: 'sd-IN', doi: 'hi-IN',
    brx: 'as-IN', sa: 'sa-IN', mni: 'bn-IN'
  };

  const CHATBOT_I18N = {
    hi: {
      title: '🌾 किसान सारथी (Kisan Saarthi)',
      subtitle: '⚡ 24/7 लाइव कृषि मौसम AI सहायक • MoES / ICAR',
      greeting: '🌾 <strong>नमस्कार! मैं आपका किसान सारथी AI सहायक हूँ।</strong><br>अपने जिले में वर्षा का पूर्वानुमान, फसल बुवाई सलाह, आंधी-तूफान या मौसम जोखिम के बारे में कुछ भी पूछें।<br><span class="kisan-bhashini-tag">⚡ डिजिटल इंडिया भाषिणी बहुभाषी AI</span>',
      placeholder: 'बारिश, फसल, मौसम के बारे में पूछें (बोलकर या लिखकर)...',
      chips: [
        { label: '🌧️ बारिश कब होगी?', prompt: 'बारिश कब होगी? जिले में वर्षा का पूर्वानुमान क्या है?' },
        { label: '🌾 फसल बुवाई सलाह', prompt: 'क्या इस हफ्ते धान या कपास की बुवाई करना सुरक्षित है?' },
        { label: '⚡ आंधी-तूफान अलर्ट', prompt: 'अगले 30 मिनट में आंधी, तूफान या बिजली गिरने का खतरा क्या है?' },
        { label: '💧 मानसून ब्रेक स्पेल', prompt: 'अगले 7 से 30 दिनों में मानसून ब्रेक स्पेल की संभावना क्या है?' },
        { label: '🦗 कीट व रोग रोकथाम', prompt: 'धान और दलहनी फसलों में कीट व रोग की रोकथाम के उपाय क्या हैं?' }
      ],
      listenBtn: '🔊 सुनें (Listen)',
      voiceTitle: 'बोलकर पूछें / Voice Input',
      sendTitle: 'सवाल भेजें (Send)'
    },
    bn: {
      title: '🌾 কিষাণ সারথি (Kisan Saarthi)',
      subtitle: '⚡ ২৪/৭ লাইভ আবহাওয়া ও কৃষি AI সহায়ক • MoES / ICAR',
      greeting: '🌾 <strong>নমস্কার! আমি আপনার কিষাণ সারথি AI সহায়ক।</strong><br>আপনার এলাকায় বৃষ্টির পূর্বাভাস, ফসল বোনার পরামর্শ, বা আবহাওয়া সংক্রান্ত যেকোনো প্রশ্ন জিজ্ঞাসা করুন।<br><span class="kisan-bhashini-tag">⚡ ডিজিটাল ইন্ডিয়া ভাষিণী বহুভাষিক AI</span>',
      placeholder: 'বৃষ্টি, ফসল বা আবহাওয়া সম্পর্কে জিজ্ঞাসা করুন...',
      chips: [
        { label: '🌧️ বৃষ্টি কখন হবে?', prompt: 'বৃষ্টি কখন হবে? জেলায় বৃষ্টির পূর্বাভাস কী?' },
        { label: '🌾 ফসল বপন পরামর্শ', prompt: 'এই সপ্তাহে ধান বা খরিফ ফসল বোনা কি নিরাপদ?' },
        { label: '⚡ বজ্রঝড় সতর্কতা', prompt: 'আগামী ৩০ মিনিটের মধ্যে ঝড় বা বজ্রপাতের ঝুঁকি কী?' },
        { label: '💧 বর্ষা বিরতি পূর্বাভাস', prompt: 'আগামী ৭-৩০ দিনে বর্ষা বিরতির সম্ভাবনা কত?' },
        { label: '🦗 কীট নিয়ন্ত্রণ', prompt: 'ফসলে পোকা ও রোগ নিয়ন্ত্রণের প্রতিকার কী?' }
      ],
      listenBtn: '🔊 শুনুন (Listen)',
      voiceTitle: 'মুখে বলে জিজ্ঞাসা করুন',
      sendTitle: 'পাঠান'
    },
    mr: {
      title: '🌾 किसान सारथी (Kisan Saarthi)',
      subtitle: '⚡ २४/७ थेट कृषी हवामान AI सहाय्यक • MoES / ICAR',
      greeting: '🌾 <strong>नमस्कार! मी तुमचा किसान सारथी AI सहाय्यक आहे.</strong><br>तुमच्या तालुक्यातील पावसाचा अंदाज, खरीप पेरणी सल्ला किंवा हवामान धोक्यांविषयी विचारा.<br><span class="kisan-bhashini-tag">⚡ डिजिटल इंडिया भाषिणी AI</span>',
      placeholder: 'पाऊस, पीक किंवा हवामानाबद्दल विचारा (बोलून किंवा लिहून)...',
      chips: [
        { label: '🌧️ पाऊस कधी पडेल?', prompt: 'पाऊस कधी पडेल? तालुक्यात पावसाचा अंदाज काय आहे?' },
        { label: '🌾 पीक पेरणी सल्ला', prompt: 'या आठवड्यात सोयाबीन/कापूस/धान पेरणी करणे योग्य आहे का?' },
        { label: '⚡ वादळ इशारा', prompt: 'पुढील ३० मिनिटांत वादळी पाऊस आणि वीज कोसळण्याचा धोका काय आहे?' },
        { label: '💧 मान्सून खंड धोका', prompt: 'पुढील ७ ते ३० दिवसांत मान्सून खंड पडण्याची शक्यता काय?' },
        { label: '🦗 कीड नियंत्रण', prompt: 'पिकांवरील कीड व रोग नियंत्रणासाठी काय उपाय करावेत?' }
      ],
      listenBtn: '🔊 ऐका (Listen)',
      voiceTitle: 'बोलून विचारा',
      sendTitle: 'पाठवा'
    },
    te: {
      title: '🌾 కిసాన్ సారథి (Kisan Saarthi)',
      subtitle: '⚡ 24/7 లైవ్ వ్యవసాయ వాతావరణ AI సహాయకుడు • MoES / ICAR',
      greeting: '🌾 <strong>నమస్కారం! నేను మీ కిసాన్ సారథి AI సహాయకుడిని.</strong><br>స్థానిక వర్షపాతం, పంట విత్తనాల సలహా లేదా వాతావరణం గురించి ఏదైనా అడగండి.<br><span class="kisan-bhashini-tag">⚡ డిజిటల్ ఇండియా భాషిణి AI</span>',
      placeholder: 'వర్షం, పంటలు లేదా వాతావరణం గురించి అడగండి...',
      chips: [
        { label: '🌧️ వర్షం ఎప్పుడు?', prompt: 'వర్షం ఎప్పుడు పడుతుంది? జిల్లాలో వర్ష సూచన ఏమిటి?' },
        { label: '🌾 పంట విత్తే సలహా', prompt: 'ఈ వారం వరి లేదా పత్తి విత్తడం సురక్షితమేనా?' },
        { label: '⚡ తుఫాను హెచ్చరిక', prompt: 'రాబోయే 30 నిమిషాల్లో తుఫాను లేదా మెరుపుల ప్రమాదం ఉందా?' },
        { label: '💧 రుతుపవన విరామం', prompt: 'రాబోయే 7-30 రోజుల్లో వర్ష విరామం సంభవించే అవకాశం ఎంత?' },
        { label: '🦗 తెగుళ్ల నివారణ', prompt: 'పంటలలో తెగుళ్ల నివారణకు తీసుకోవలసిన జాగ్రత్తలు ఏమిటి?' }
      ],
      listenBtn: '🔊 వినండి (Listen)',
      voiceTitle: 'మాట్లాడి అడగండి',
      sendTitle: 'పంపండి'
    },
    ta: {
      title: '🌾 கிசான் சாரதி (Kisan Saarthi)',
      subtitle: '⚡ 24/7 நேரடி வேளாண் வானிலை AI உதவியாளர் • MoES / ICAR',
      greeting: '🌾 <strong>வணக்கம்! நான் உங்கள் கிசான் சாரதி AI உதவியாளர்.</strong><br>மழை முன்னறிவிப்பு, விதைப்பு ஆலோசனை அல்லது வானிலை குறித்து எதையும் கேளுங்கள்.<br><span class="kisan-bhashini-tag">⚡ டிஜிட்டல் இந்தியா பாஷினி AI</span>',
      placeholder: 'மழை, பயிர் அல்லது வானிலை பற்றி கேளுங்கள்...',
      chips: [
        { label: '🌧️ மழை எப்போது?', prompt: 'மழை எப்போது வரும்? மாவட்டத்தின் மழை முன்னறிவிப்பு என்ன?' },
        { label: '🌾 விதைப்பு ஆலோசனை', prompt: 'இந்த வாரம் நெல் அல்லது பருத்தி விதைப்பது பாதுகாப்பானதா?' },
        { label: '⚡ புயல் எச்சரிக்கை', prompt: 'அடுத்த 30 நிமிடங்களில் புயல் அல்லது மின்னல் ஆபத்து உள்ளதா?' },
        { label: '💧 பருவமழை இடைவெளி', prompt: 'அடுத்த 7-30 நாட்களில் பருவமழை இடைவெளிக்கு வாய்ப்பு உள்ளதா?' },
        { label: '🦗 பூச்சி கட்டுப்பாடு', prompt: 'பயிர்களில் பூச்சி தாக்குதலை தடுக்கும் முறைகள் யாவை?' }
      ],
      listenBtn: '🔊 கேளுங்கள் (Listen)',
      voiceTitle: 'பேசி கேளுங்கள்',
      sendTitle: 'அனுப்பவும்'
    },
    gu: {
      title: '🌾 કિસાન સારથિ (Kisan Saarthi)',
      subtitle: '⚡ ૨૪/૭ લાઈવ કૃષિ હવામાન AI સહાયક • MoES / ICAR',
      greeting: '🌾 <strong>નમસ્કાર! હું તમારો કિસાન સારથિ AI સહાયક છું.</strong><br>તમારા જિલ્લામાં વરસાદની આગાહી, વાવણી સલાહ અથવા હવામાન વિશે કંઈપણ પૂછો.<br><span class="kisan-bhashini-tag">⚡ ડિજિટલ ઇન્ડિયા ભાષિણી AI</span>',
      placeholder: 'વરસાદ, પાક કે હવામાન વિશે પૂછો...',
      chips: [
        { label: '🌧️ વરસાદ ક્યારે પડશે?', prompt: 'વરસાદ ક્યારે પડશે? જિલ્લામાં વરસાદની આગાહી શું છે?' },
        { label: '🌾 વાવણી સલાહ', prompt: 'શું આ અઠવાડિયે કપાસ કે ડાંગર વાવવી સુરક્ષિત છે?' },
        { label: '⚡ વાવાઝોડું એલર્ટ', prompt: 'આગામી 30 મિનિટમાં વાવાઝોડું કે વીજળી પડવાનું જોખમ કેટલું છે?' },
        { label: '💧 ચોમાસુ વિરામ', prompt: 'આગામી 7-30 દિવસોમાં વરસાદના વિરામની શક્યતા કેટલી છે?' },
        { label: '🦗 જીવાત નિયંત્રણ', prompt: 'પાકમાં જીવાત અને રોગ નિયંત્રણ માટે શું પગલાં લેવા?' }
      ],
      listenBtn: '🔊 સાંભળો (Listen)',
      voiceTitle: 'બોલીને પૂછો',
      sendTitle: 'મોકલો'
    },
    pa: {
      title: '🌾 ਕਿਸਾਨ ਸਾਰਥੀ (Kisan Saarthi)',
      subtitle: '⚡ 24/7 ਲਾਈਵ ਖੇਤੀ ਮੌਸਮ AI ਸਹਾਇਕ • MoES / ICAR',
      greeting: '🌾 <strong>ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਡਾ ਕਿਸਾਨ ਸਾਰਥੀ AI ਸਹਾਇਕ ਹਾਂ।</strong><br>ਆਪਣੇ ਜ਼ਿਲ੍ਹੇ ਵਿੱਚ ਮੀਂਹ ਦੀ ਪੇਸ਼ੀਨਗੋਈ, ਬਿਜਾਈ ਦੀ ਸਲਾਹ ਜਾਂ ਮੌਸਮ ਬਾਰੇ ਕੁਝ ਵੀ ਪੁੱਛੋ।<br><span class="kisan-bhashini-tag">⚡ ਡਿਜੀਟਲ ਇੰਡੀਆ ਭਾਸ਼ਿਨੀ AI</span>',
      placeholder: 'ਮੀਂਹ, ਫ਼ਸਲ ਜਾਂ ਮੌਸਮ ਬਾਰੇ ਪੁੱਛੋ...',
      chips: [
        { label: '🌧️ ਮੀਂਹ ਕਦੋਂ ਪਵੇਗਾ?', prompt: 'ਮੀਂਹ ਕਦੋਂ ਪਵੇਗਾ? ਜ਼ਿਲ੍ਹੇ ਵਿੱਚ ਮੀਂਹ ਦੀ ਪੇਸ਼ੀਨਗੋਈ ਕੀ ਹੈ?' },
        { label: '🌾 ਬਿਜਾਈ ਦੀ ਸਲਾਹ', prompt: 'ਕੀ ਇਸ ਹਫ਼ਤੇ ਝੋਨਾ ਜਾਂ ਨਰਮਾ ਬੀਜਣਾ ਸੁਰੱਖਿਅਤ ਹੈ?' },
        { label: '⚡ ਤੂਫ਼ਾਨ ਅਲਰਟ', prompt: 'ਅਗਲੇ 30 ਮਿੰਟਾਂ ਵਿੱਚ ਤੂਫ਼ਾਨ ਜਾਂ ਅਸਮਾਨੀ ਬਿਜਲੀ ਦਾ ਕੀ ਖ਼ਤਰਾ ਹੈ?' },
        { label: '💧 ਮਾਨਸੂਨ ਬ੍ਰੇਕ', prompt: 'ਅਗਲੇ 7 ਤੋਂ 30 ਦਿਨਾਂ ਵਿੱਚ ਮਾਨਸੂਨ ਬ੍ਰੇਕ ਦੀ ਕੀ ਸੰਭਾਵਨਾ ਹੈ?' },
        { label: '🦗 ਕੀਟ ਰੋਕਥਾਮ', prompt: 'ਫ਼ਸਲਾਂ ਵਿੱਚ ਕੀੜਿਆਂ ਅਤੇ ਬਿਮਾਰੀਆਂ ਤੋਂ ਬਚਾਅ ਦੇ ਕੀ ਉਪਾਅ ਹਨ?' }
      ],
      listenBtn: '🔊 ਸੁਣੋ (Listen)',
      voiceTitle: 'ਬੋਲ ਕੇ ਪੁੱਛੋ',
      sendTitle: 'ਭੇਜੋ'
    },
    en: {
      title: '🌾 Kisan Saarthi (किसान सारथी)',
      subtitle: '⚡ 24/7 Live Agromet AI Copilot • MoES / ICAR',
      greeting: '🌾 <strong>Namaskar! I am your Kisan Saarthi AI Assistant.</strong><br>Ask me anything about local rainfall forecasts, crop sowing advisory, thunderstorm nowcasts, or weather risks in your district.<br><span class="kisan-bhashini-tag">⚡ Digital India Bhashini Multilingual AI</span>',
      placeholder: 'Ask Kisan Saarthi about rainfall, crops, weather... (speak or type)',
      chips: [
        { label: '🌧️ When will it rain?', prompt: 'When will it rain? What is the district rainfall forecast?' },
        { label: '🌾 Sowing Advisory', prompt: 'Is it safe to sow paddy or cotton this week?' },
        { label: '⚡ Storm Alert', prompt: 'What is the thunderstorm and lightning risk in the next 30 minutes?' },
        { label: '💧 Monsoon Break Spell', prompt: 'What is the probability of a monsoon break spell in the next 7-30 days?' },
        { label: '🦗 Pest Prevention', prompt: 'What are the recommended prevention measures for crop pests and diseases?' }
      ],
      listenBtn: '🔊 Listen',
      voiceTitle: 'Voice Input / बोलकर पूछें',
      sendTitle: 'Send Question'
    }
  };

  function getActiveDict() {
    const cur = (window.appState && window.appState.currentLang) || 'en';
    return CHATBOT_I18N[cur] || CHATBOT_I18N['en'];
  }

  // Initialize Speech Recognition if supported
  function initSpeech() {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRec) {
      speechRecognition = new SpeechRec();
      speechRecognition.continuous = false;
      speechRecognition.interimResults = false;

      speechRecognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        const input = document.getElementById('agentInsightInput');
        if (input && transcript) {
          input.value = transcript;
          submitPrompt(transcript, true);
        }
        stopListening();
      };

      speechRecognition.onerror = function() {
        stopListening();
      };

      speechRecognition.onend = function() {
        stopListening();
      };
    }
  }

  function startListening() {
    if (!speechRecognition) {
      initSpeech();
    }
    if (!speechRecognition) {
      alert(window.appState?.currentLang === 'hi' 
        ? 'आपके ब्राउज़र में आवाज़ पहचान समर्थित नहीं है।' 
        : 'Speech recognition is not supported in this browser.');
      return;
    }
    try {
      const curLang = (window.appState && window.appState.currentLang) || 'en';
      speechRecognition.lang = TTS_LANG_MAP[curLang] || 'en-IN';
      speechRecognition.start();
      isListening = true;
      updateMicBtnState(true);
    } catch (_) {
      stopListening();
    }
  }

  function stopListening() {
    if (speechRecognition && isListening) {
      try { speechRecognition.stop(); } catch (_) {}
    }
    isListening = false;
    updateMicBtnState(false);
  }

  function toggleVoice() {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  }

  function updateMicBtnState(listening) {
    const micBtn = document.getElementById('btnAgentVoiceMic');
    if (micBtn) {
      const dict = getActiveDict();
      if (listening) {
        micBtn.classList.add('recording');
        micBtn.title = 'सुन रहा हूँ... बोलिए (Listening...)';
      } else {
        micBtn.classList.remove('recording');
        micBtn.title = dict.voiceTitle || 'बोलकर पूछें / Voice Input';
      }
    }
  }

  // Multilingual Text-to-Speech (TTS)
  function speakBotResponse(text) {
    const curLang = (window.appState && window.appState.currentLang) || 'en';
    if (typeof window.speakText === 'function') {
      window.speakText(text, curLang);
    } else if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const cleanText = text.replace(/<[^>]*>/g, '').replace(/[*#_`]/g, '');
      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.lang = TTS_LANG_MAP[curLang] || 'en-IN';
      utterance.rate = 0.95;
      window.speechSynthesis.speak(utterance);
    }
  }

  // Dynamically update chatbot texts according to user's selected language
  function updateAgentInsightLanguage() {
    const dict = getActiveDict();

    const titleEl = document.querySelector('#agent-insight-modal .kisan-header-title span');
    if (titleEl && dict.title) titleEl.textContent = dict.title;

    const subEl = document.querySelector('#agent-insight-modal .kisan-header-sub');
    if (subEl && dict.subtitle) subEl.textContent = dict.subtitle;

    const input = document.getElementById('agentInsightInput');
    if (input && dict.placeholder) input.placeholder = dict.placeholder;

    const sendBtn = document.getElementById('btnAgentStreamSend');
    if (sendBtn && dict.sendTitle) sendBtn.title = dict.sendTitle;

    const micBtn = document.getElementById('btnAgentVoiceMic');
    if (micBtn && dict.voiceTitle) micBtn.title = dict.voiceTitle;

    // Update Chips
    const chipsTray = document.querySelector('.kisan-chips-tray');
    if (chipsTray && dict.chips && dict.chips.length) {
      chipsTray.innerHTML = dict.chips.map(c => 
        `<button class="kisan-chip" data-prompt="${escapeHtml(c.prompt)}">${c.label}</button>`
      ).join('');
      attachChipListeners();
    }

    // Update Initial Greeting if no user conversation started yet
    const msgsContainer = document.getElementById('agentInsightMessages');
    if (msgsContainer) {
      const userMsgs = msgsContainer.querySelectorAll('.kisan-msg-row.user');
      if (userMsgs.length === 0) {
        const initialBotMsg = msgsContainer.querySelector('.agent-msg.bot');
        if (initialBotMsg && dict.greeting) {
          initialBotMsg.innerHTML = dict.greeting;
        }
      }
    }

    if (speechRecognition) {
      const curLang = (window.appState && window.appState.currentLang) || 'en';
      speechRecognition.lang = TTS_LANG_MAP[curLang] || 'en-IN';
    }
  }

  function attachChipListeners() {
    const chips = document.querySelectorAll('#agent-insight-widget .kisan-chip');
    chips.forEach(chip => {
      chip.addEventListener('click', () => {
        const prompt = chip.getAttribute('data-prompt');
        if (prompt) submitPrompt(prompt);
      });
    });
  }

  // Initialize UI once DOM is ready
  function initAgentInsightPanel() {
    if (document.getElementById('agent-insight-widget')) return;

    initSpeech();

    // 1. Inject Styles with pure Kisan Saarthi Aesthetic
    const styleEl = document.createElement('style');
    styleEl.id = 'agent-insight-panel-styles';
    styleEl.textContent = `
      /* Kisan Saarthi Live Streaming Modal Window */
      #agent-insight-modal {
        position: fixed;
        bottom: 24px;
        right: 24px;
        width: 420px;
        max-width: calc(100vw - 36px);
        height: 600px;
        max-height: calc(100vh - 48px);
        background: #ffffff;
        border: 1.5px solid #bbf7d0;
        border-radius: 18px;
        box-shadow: 0 24px 50px rgba(15, 23, 42, 0.22), 0 6px 20px rgba(21, 128, 61, 0.15);
        z-index: 99999;
        display: none;
        flex-direction: column;
        overflow: hidden;
        font-family: inherit;
        color: #0f172a;
        animation: kisanSlideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      }
      @keyframes kisanSlideUp {
        from { opacity: 0; transform: translateY(16px) scale(0.97); }
        to { opacity: 1; transform: translateY(0) scale(1); }
      }
      .kisan-modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 13px 16px;
        background: linear-gradient(135deg, #15803d 0%, #166534 100%);
        border-bottom: 1px solid #14532d;
        color: #ffffff;
      }
      .kisan-header-left {
        display: flex;
        align-items: center;
        gap: 10px;
      }
      .kisan-header-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        border: 2px solid #86efac;
        object-fit: cover;
        display: block;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        flex-shrink: 0;
      }
      .kisan-header-titles {
        display: flex;
        flex-direction: column;
      }
      .kisan-header-title {
        font-size: 14.5px;
        font-weight: 800;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 6px;
        line-height: 1.2;
      }
      .kisan-header-sub {
        font-size: 11px;
        color: #dcfce7;
        font-weight: 600;
        letter-spacing: 0.2px;
      }
      .kisan-modal-close {
        background: rgba(255, 255, 255, 0.15);
        border: none;
        color: #ffffff;
        font-size: 14px;
        font-weight: 800;
        cursor: pointer;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background 0.2s, transform 0.15s;
      }
      .kisan-modal-close:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: scale(1.08);
      }

      /* Quick Prompts Tray */
      .kisan-chips-tray {
        display: flex;
        gap: 7px;
        padding: 9px 12px;
        overflow-x: auto;
        white-space: nowrap;
        background: #f0fdf4;
        border-bottom: 1px solid #bbf7d0;
        scrollbar-width: none;
      }
      .kisan-chips-tray::-webkit-scrollbar { display: none; }
      .kisan-chip {
        background: #ffffff;
        border: 1px solid #86efac;
        border-radius: 14px;
        padding: 5px 11px;
        font-size: 11.5px;
        font-weight: 600;
        color: #166534;
        cursor: pointer;
        transition: all 0.15s ease;
        flex-shrink: 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
      }
      .kisan-chip:hover {
        background: #dcfce7;
        border-color: #15803d;
        color: #14532d;
        transform: translateY(-1px);
        box-shadow: 0 3px 6px rgba(21, 128, 61, 0.15);
      }

      /* Messages Area */
      .kisan-messages-container {
        flex: 1;
        overflow-y: auto;
        padding: 14px 16px;
        display: flex;
        flex-direction: column;
        gap: 12px;
        background: #f8fafc;
      }
      .kisan-msg-row {
        display: flex;
        gap: 10px;
        align-items: flex-start;
      }
      .kisan-msg-row.user {
        justify-content: flex-end;
      }
      .kisan-bot-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        border: 1.5px solid #22c55e;
        object-fit: cover;
        flex-shrink: 0;
        margin-top: 2px;
        box-shadow: 0 2px 6px rgba(34, 197, 94, 0.2);
      }
      .agent-msg {
        max-width: 86%;
        padding: 10px 14px;
        border-radius: 14px;
        font-size: 13px;
        line-height: 1.55;
        word-break: break-word;
      }
      .agent-msg.user {
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%);
        color: #ffffff;
        border-bottom-right-radius: 4px;
        box-shadow: 0 2px 8px rgba(21, 128, 61, 0.25);
        align-self: flex-end;
      }
      .agent-msg.bot {
        background: #ffffff;
        border: 1.5px solid #bbf7d0;
        color: #0f172a;
        border-bottom-left-radius: 4px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        position: relative;
      }
      .kisan-bhashini-tag {
        display: inline-block;
        margin-top: 6px;
        font-size: 10px;
        background: #dcfce7;
        color: #15803d;
        border: 1px solid #86efac;
        padding: 2px 7px;
        border-radius: 8px;
        font-weight: 700;
      }
      .kisan-speaker-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: #f0fdf4;
        border: 1px solid #86efac;
        color: #15803d;
        border-radius: 6px;
        padding: 3px 8px;
        font-size: 11px;
        font-weight: 700;
        cursor: pointer;
        margin-top: 7px;
        transition: all 0.15s;
        gap: 4px;
      }
      .kisan-speaker-btn:hover {
        background: #dcfce7;
        color: #166534;
        border-color: #15803d;
      }
      .agent-cursor {
        display: inline-block;
        width: 6px;
        height: 13px;
        background: #15803d;
        margin-left: 3px;
        vertical-align: middle;
        animation: kisanBlink 0.8s infinite;
      }
      @keyframes kisanBlink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
      }

      /* Input Bar */
      .kisan-input-bar {
        display: flex;
        gap: 8px;
        align-items: center;
        padding: 10px 14px;
        background: #ffffff;
        border-top: 1px solid #e2e8f0;
      }
      #agentInsightInput {
        flex: 1;
        background: #f8fafc;
        border: 1.5px solid #cbd5e1;
        border-radius: 22px;
        padding: 9px 15px;
        color: #0f172a;
        font-size: 12.5px;
        outline: none;
        transition: all 0.2s;
        font-family: inherit;
      }
      #agentInsightInput:focus {
        border-color: #15803d;
        background: #ffffff;
        box-shadow: 0 0 0 3px rgba(21, 128, 61, 0.12);
      }
      #btnAgentVoiceMic {
        background: #f0fdf4;
        border: 1.5px solid #86efac;
        color: #15803d;
        border-radius: 50%;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 15px;
        transition: all 0.2s;
        flex-shrink: 0;
      }
      #btnAgentVoiceMic:hover {
        background: #dcfce7;
        border-color: #15803d;
        transform: scale(1.05);
      }
      #btnAgentVoiceMic.recording {
        background: #fee2e2;
        border-color: #ef4444;
        color: #b91c1c;
        animation: micPulse 1.2s infinite;
      }
      @keyframes micPulse {
        0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
        50% { transform: scale(1.1); box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }
      }
      #btnAgentStreamSend {
        background: #15803d;
        color: #ffffff;
        border: none;
        border-radius: 50%;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s;
        flex-shrink: 0;
        font-size: 14px;
        box-shadow: 0 2px 6px rgba(21, 128, 61, 0.25);
      }
      #btnAgentStreamSend:hover {
        background: #166534;
        transform: scale(1.06);
      }
    `;
    document.head.appendChild(styleEl);

    const initialDict = getActiveDict();

    // 2. Inject Modal HTML (Launcher removed from viewport for zero UI obstruction)
    const widgetRoot = document.createElement('div');
    widgetRoot.id = 'agent-insight-widget';
    widgetRoot.innerHTML = `
      <!-- Glassmorphic Modal Window (Triggered from Top Nav, Home Cards & Quick Links) -->
      <div id="agent-insight-modal" role="dialog" aria-label="Kisan Saarthi AI Assistant">
        <div class="kisan-modal-header">
          <div class="kisan-header-left">
            <img src="/assets/rituiq_kisan_ai_logo.png" alt="Kisan Saarthi" class="kisan-header-avatar" />
            <div class="kisan-header-titles">
              <div class="kisan-header-title">
                <span>${initialDict.title}</span>
              </div>
              <div class="kisan-header-sub">${initialDict.subtitle}</div>
            </div>
          </div>
          <button class="kisan-modal-close" id="btnAgentModalClose" title="Close Panel">✕</button>
        </div>

        <!-- Quick Prompts Tray -->
        <div class="kisan-chips-tray">
          ${initialDict.chips.map(c => `<button class="kisan-chip" data-prompt="${escapeHtml(c.prompt)}">${c.label}</button>`).join('')}
        </div>

        <!-- Messages Area -->
        <div class="kisan-messages-container" id="agentInsightMessages">
          <div class="kisan-msg-row">
            <img src="/assets/rituiq_kisan_ai_logo.png" alt="Kisan Saarthi" class="kisan-bot-avatar" />
            <div class="agent-msg bot">
              ${initialDict.greeting}
            </div>
          </div>
        </div>

        <!-- Input Bar -->
        <div class="kisan-input-bar">
          <button id="btnAgentVoiceMic" type="button" title="${initialDict.voiceTitle}">🎙️</button>
          <input type="text" id="agentInsightInput" placeholder="${initialDict.placeholder}" />
          <button id="btnAgentStreamSend" type="button" title="${initialDict.sendTitle}">➤</button>
        </div>
      </div>
    `;
    document.body.appendChild(widgetRoot);

    // 3. Attach Listeners
    const launcher = document.getElementById('agent-insight-launcher');
    const closeBtn = document.getElementById('btnAgentModalClose');
    const sendBtn = document.getElementById('btnAgentStreamSend');
    const micBtn = document.getElementById('btnAgentVoiceMic');
    const input = document.getElementById('agentInsightInput');

    if (launcher) {
      launcher.addEventListener('click', () => toggleModal());
    }
    if (closeBtn) {
      closeBtn.addEventListener('click', () => closeModal());
    }

    // Escape key closes modal
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeModal();
    });

    if (micBtn) {
      micBtn.addEventListener('click', toggleVoice);
    }

    sendBtn.addEventListener('click', () => {
      const text = input.value.trim();
      if (text) submitPrompt(text);
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const text = input.value.trim();
        if (text) submitPrompt(text);
      }
    });

    attachChipListeners();
  }

  function toggleModal(forceState) {
    const modal = document.getElementById('agent-insight-modal');
    if (!modal) return;
    const shouldOpen = forceState !== undefined ? forceState : (modal.style.display !== 'flex');
    if (shouldOpen) {
      updateAgentInsightLanguage();
      modal.style.display = 'flex';
      const input = document.getElementById('agentInsightInput');
      if (input) setTimeout(() => input.focus(), 120);
    } else {
      closeModal();
    }
  }

  function closeModal() {
    const modal = document.getElementById('agent-insight-modal');
    if (modal) modal.style.display = 'none';
    stopListening();
  }

  function openWithPrompt(promptText) {
    toggleModal(true);
    if (promptText) {
      setTimeout(() => {
        submitPrompt(promptText);
      }, 150);
    }
  }

  // Real-time Stream Consumer from /api/agent (Agent37 Powered with RAG Fallback)
  async function submitPrompt(promptText, requestedByVoice = false) {
    if (isStreaming) {
      if (activeAbortController) activeAbortController.abort();
    }

    const messagesContainer = document.getElementById('agentInsightMessages');
    const input = document.getElementById('agentInsightInput');
    if (!messagesContainer || !promptText.trim()) return;

    if (input) input.value = '';

    // Append User Message
    const userRow = document.createElement('div');
    userRow.className = 'kisan-msg-row user';
    userRow.innerHTML = `<div class="agent-msg user">${escapeHtml(promptText)}</div>`;
    messagesContainer.appendChild(userRow);

    // Append Bot Container with Kisan Saarthi Avatar & Streaming Cursor
    const botRow = document.createElement('div');
    botRow.className = 'kisan-msg-row';
    botRow.innerHTML = `
      <img src="/assets/rituiq_kisan_ai_logo.png" alt="Kisan Saarthi" class="kisan-bot-avatar" />
      <div class="agent-msg bot">
        <span class="bot-text"></span><span class="agent-cursor"></span>
      </div>
    `;
    messagesContainer.appendChild(botRow);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    const botMsg = botRow.querySelector('.agent-msg.bot');
    const textSpan = botMsg.querySelector('.bot-text');
    const cursor = botMsg.querySelector('.agent-cursor');

    isStreaming = true;
    activeAbortController = new AbortController();

    const curLang = (window.appState && window.appState.currentLang) || 'en';
    const curBlock = (window.appState && window.appState.locationHierarchy && window.appState.locationHierarchy.blockId) || 'MH_YVT_01';
    const dict = getActiveDict();

    try {
      const response = await fetch('/api/agent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream, application/json'
        },
        body: JSON.stringify({
          input: promptText,
          stream: true,
          block_id: curBlock,
          language: curLang
        }),
        signal: activeAbortController.signal
      });

      if (!response.ok) {
        throw new Error(`Server returned HTTP ${response.status}`);
      }

      if (!response.body) {
        throw new Error('ReadableStream not supported by browser');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let buffer = '';
      let accumulatedText = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // keep last incomplete line

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed || trimmed.startsWith(':')) continue;

          if (trimmed === 'data: [DONE]') {
            break;
          }

          if (trimmed.startsWith('data: ')) {
            const dataStr = trimmed.slice(6);
            try {
              const dataObj = JSON.parse(dataStr);
              if (dataObj.text) {
                accumulatedText += dataObj.text;
                textSpan.textContent = accumulatedText;
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
              } else if (dataObj.error) {
                textSpan.textContent += ` [Error: ${dataObj.error}]`;
              }
            } catch (_) {
              // Raw text chunk fallback
              accumulatedText += dataStr;
              textSpan.textContent = accumulatedText;
              messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
          }
        }
      }

      // Add audio speaker button on completed response
      if (accumulatedText.trim()) {
        const speakerBtn = document.createElement('button');
        speakerBtn.type = 'button';
        speakerBtn.className = 'kisan-speaker-btn';
        speakerBtn.innerHTML = `${dict.listenBtn || '🔊 Listen'}`;
        speakerBtn.onclick = function() {
          speakBotResponse(accumulatedText);
        };
        botMsg.appendChild(document.createElement('br'));
        botMsg.appendChild(speakerBtn);

        // If requested by voice, speak response automatically
        if (requestedByVoice) {
          speakBotResponse(accumulatedText);
        }
      }

    } catch (err) {
      if (err.name === 'AbortError') {
        textSpan.textContent += ' [Stream stopped]';
      } else {
        textSpan.textContent += `\n[Stream Error: ${err.message}]`;
      }
    } finally {
      isStreaming = false;
      activeAbortController = null;
      if (cursor) cursor.remove();
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Mount on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAgentInsightPanel);
  } else {
    initAgentInsightPanel();
  }

  // Global Exports: Named Kisan Saarthi
  window.openKisanSaarthiChat = function(promptText) {
    if (promptText) {
      openWithPrompt(promptText);
    } else {
      toggleModal(true);
    }
  };

  window.openKisanSaarthiVoice = function() {
    toggleModal(true);
    setTimeout(() => {
      startListening();
    }, 200);
  };

  window.updateAgentInsightLanguage = updateAgentInsightLanguage;

  window.KisanSaarthiAgent = {
    open: () => toggleModal(true),
    close: closeModal,
    toggle: toggleModal,
    submit: submitPrompt,
    openWithPrompt: openWithPrompt,
    startVoice: startListening,
    updateLanguage: updateAgentInsightLanguage
  };

  // Backwards compatibility alias
  window.AgentInsightPanel = window.KisanSaarthiAgent;

})(window);
