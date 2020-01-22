var pieChart = "";
var pieChart2 = "";
var pieChart3 = "";

$(document).ready(function(){
  $("#indTable").hide();
  $('#indTable2').hide();
  $('#indTable3').hide();
  $("#indTable4").hide();
  $('#indTable5').hide();
  $('#indTable6').hide();
  $("#indTable7").hide();
  $('#indTable8').hide();
  $('#indTable9').hide();


  $("#info1").hide();
  $("#info2").hide();
  $("#info3").hide();
  $("#info4").hide();
  $("#info5").hide();
  $("#info6").hide();

  $(".processing").hide();

  pieChart =  new Chart(document.getElementById("pie-chart"), {
    type: 'pie',
    data: {
      labels: ["Offensive", "Not Offensive"],
      datasets: [{
        label: "Offensiveness distribution",
        backgroundColor: ["#D8401F", "#1F70D8"],
        data: [0,0]
      }]
    },
    options: {
       tooltips: {
    callbacks: {
      label: function(tooltipItem, data) {
        var dataset = data.datasets[tooltipItem.datasetIndex];
        var meta = dataset._meta[Object.keys(dataset._meta)[0]];
        var total = meta.total;
        var currentValue = dataset.data[tooltipItem.index];
        var percentage = parseFloat((currentValue/total*100).toFixed(1));
        return currentValue + ' (' + percentage + '%)';
      },
      title: function(tooltipItem, data) {
        return data.labels[tooltipItem[0].index];
      }
    }
  },
      title: {
        display: true,
        text: 'Offensiveness distribution'
      }
    }
  });
  $("#pie-chart").hide();

    pieChart2 =  new Chart(document.getElementById("pie-chart2"), {
    type: 'pie',
    data: {
      labels: ["Advertisement", "Not Advertisement"],
      datasets: [{
        label: "Advertisement distribution",
        backgroundColor: ["#D8401F", "#1F70D8"],
        data: [0,0]
      }]
    },
    options: {
       tooltips: {
    callbacks: {
      label: function(tooltipItem, data) {
        var dataset = data.datasets[tooltipItem.datasetIndex];
        var meta = dataset._meta[Object.keys(dataset._meta)[0]];
        var total = meta.total;
        var currentValue = dataset.data[tooltipItem.index];
        var percentage = parseFloat((currentValue/total*100).toFixed(1));
        return currentValue + ' (' + percentage + '%)';
      },
      title: function(tooltipItem, data) {
        return data.labels[tooltipItem[0].index];
      }
    }
  },
      title: {
        display: true,
        text: 'Advertisement distribution'
      }
    }
  });
  $("#pie-chart2").hide();

  pieChart3 =  new Chart(document.getElementById("pie-chart3"), {
    type: 'pie',
    data: {
      labels: ["Hate-speech", "Not Hate-speech"],
      datasets: [{
        label: "Hate-speech distribution",
        backgroundColor: ["#D8401F", "#1F70D8"],
        data: [0,0]
      }]
    },
    options: {
       tooltips: {
    callbacks: {
      label: function(tooltipItem, data) {
        var dataset = data.datasets[tooltipItem.datasetIndex];
        var meta = dataset._meta[Object.keys(dataset._meta)[0]];
        var total = meta.total;
        var currentValue = dataset.data[tooltipItem.index];
        var percentage = parseFloat((currentValue/total*100).toFixed(1));
        return currentValue + ' (' + percentage + '%)';
      },
      title: function(tooltipItem, data) {
        return data.labels[tooltipItem[0].index];
      }
    }
  },
      title: {
        display: true,
        text: 'Hate-speech distribution'
      }
    }
  });
  $("#pie-chart3").hide();

});

var queries = [
"@QF",
"@ajarabic",
"@QF OR @ajarabic",
"#Qatar"
]

var offensiveSamples = [
"يا صبر الأرض عليك يا مدرب يا حثاله المشكلة يدفعون ملايين لمدرب سبااااااك",
"@USER وجمهور الاهلى لن ينسى موقفكم يا اتحاد العار يا مرتزقة يا مرتشين والحساب قريبا وياريت ماتتمسحش فى جمهور الاهلى عشان الكلاب اللى زيك جمهور الاهلى داس عليهم بالجزمة خلاص لان ده مقامك يا قذر",
"@USER @USER @USER ارجع لتاريخك وتاريخ ملك اسياء وتعرف من الوضيع يا ابو ثلاثه دوري يا محلي",
"@USER يارب يا كريم يا سميع يا بصير انك تحرم نادي الهلال الوضيع المنبطح الدوري وينهزم قدام التعاون والاتفاق والشباب امين يارب 🙌🏽",
"@USER @USER الله يقلعكم يالبدو يا مجرمين يا خراب المجتمعات ... طفيليات غير نافعه فقط تضر المجتمعات ابوكم ابو قبايلكم الزق",
"@USER يا كلب الصهاينة يا عميل الفرس أنت عبد من عبيد نعال الحكام الظلمة و القتلة، أنت لا تساوي ذرة رمل في شسع نعال الرجال يا أقذر خلق الله يا وقح.",
"قصدي وسط البلاد يا وسخين يا حقيرين يا نذلين ...<LF>احياء سكنيه و ناس مدنية ...<LF>تفو و حسبي الله و نعم الوكيل في كل من كان السبب💔",
"يا كريه يا لعين يا مُستفز يا سافل .. والله ماتشم الدوري URL",
"@USER روح يا ابن الزنا يا كلب يا فاسد انت وحكومتك ورئيسك يا زوامل يا عيال شحيبر حكومة ورئسة",
"@USER القوات راكبه امايتكن واحد واحد من كبيركن ل صفيركن . و صرمايه كل فرد و وزير او نائب اشرف من راس بياتكن و يا بجم يا حواش انتم سرطان المجتمع اللبناني .",
"RT @USER: يا رب الأفضل للأفضل.. يا رب الطيب للطيب.. يا رب النوايا لأهل النوايـا.. يا رب الخير كلـه لقلوبنا والجمال يتخلل أيامنا والر…",
"@USER حبيبي يا كابتن عصام يا جميل مساءك سعيد",
"ايش الاكل الحلو ذا ياسُميه تسلم يدك ياعسل ياقشطه ياحلوه ياسُكره يا طباخه يا فنانه يا كل شي💛.",
"يا بسمةَ الصّبحِ يا فألي ويا أملي ،<LF>يا نغمةَ الطيرِ إن غنىٰ بأسماعي 💛🕊<LF>URL",
"اللهم مغفرتك أوسع من ذنوبي ، ورحمتك أرجي عندي من عملي , <LF>سبحانك لا إله غيرك أغفر لي ذنبي وأصلح لي عملي إنك تغفر الذنوب لمن تشاء ,<LF>وأنت الغفور الرحيم يا غفار أغفر لي يا تواب تب علي يا رحمن أرحمني يا عفو أعفو عني يا رؤف أرءف بي .. - <LF> w: URL URL",
"يا ساحِرة البسمة يا حبيبتي أنا .",
"انا في حلم ولا وين يا رب لك الحمد يا رب💛💛💛💛💛💛💛",
"يا حي يا قيوم برحمتك استغيث يا ودود يا ودود ياودود يا ذا العرش المجيد يا رحمن يا رحيم يا فعالا لما تريد اللهم اني اسألك بعزك الذي لا يرام ومُلكك الذي لا يضام ونورك الذي ملأ ارجاء عرشك ان تقضي حاجتي يارب يا كريم عاجل بالاجابه يارب وراضي قلبي وراضيني وفرحني واجبر بخاطري يارب 🤲🏻",
"يا ملائكية الخدين ، يا حوراء العينين <LF>يا غجرية الشعر ، يا فواحة العبير ويا غذاء الروح",
"فى مثل هذا اليوم فى مثل هذه الساعة و بعد صلاة الظهر منذ عام بالتمام و الكمال واريتك فى التراب يا أغلى الناس يا اعز الناس، رحمة الله عليك يا أبي، اللهم اغفر له وارحمه واسكنه فسيح جناتك و اكرم منزله و ابعثه مع... URL"
]

var adSamples = [
"@USER 👑🐝👑🐝👑🐝👑🐝👑🐝<LF>-امن🤛 صحي<LF>- تأخير القذف<LF><LF>👌بخاخ سوبر دراجون 👌<LF>-ليس له اضرار جانبية<LF>-ياخر القذف ما بين 20 ل 30 دقيقة<LF><LF>للتواصل واتساب :<LF>URL<LF>WFaHOQ",
"@USER 🔷🔷 منتج طبيعي من نبات الالوفيرا والعسل #كلين9 🔷<LF> تخلص من دهون جسمك مرة والي الابد<LF><LF>🇸🇦 🇰🇼<LF><LF>🇴🇲 🇦🇪<LF> لا تعرض حياتك لخطر ستندم عليه لاحقا بسبب السمنة <LF><LF>للتواصل عبر الخااص<LF>URL<LF>BMFkfb",
"@USER كلين9<LF>افضل برنامج تخسيس في الخليج🔱<LF><LF> فيت وان ينزل 25 كيلو خلال شهر🕑<LF>💪🍊🍐💪<LF>كلين 9 الوسط ينزل15كيلو خلال 21💪🍊🍏🍎🍋<LF>💪🍊🍏🍎🍋🍐<LF>كلين المصغر ينزل 9كيلو خلال 12يوم<LF>💪🍋🍐💪<LF>URL<LF>5Liy",
"@USER احصل علي حياه زوجيه سعيدة مع منتج جين شيا 😍<LF>المنتج يعمل على<LF>🌲تقويه الانتصاب<LF>🌲تأخير سرعة القذف لفترات اطول<LF>🌲زيادة فترة الجماع وزيادة كمية السائل<LF>🌲تحسين صحة البروستاتا<LF>للطلب والاستفسار عبر الواتساب<LF>URL<LF>او<LF>عبر صفحة الدكتورة الشخصية @USER<LF>tffW URL",
"@USER @USER * مجموعة علَاج البَـواسِير * الامرِيكية<LF><LF>علاج البَواسِير الداخلية والخارجية<LF>النتائج مضمونه وامنة وفعالة<LF>منتجات اعشاب طبيعية ومكملات غذائية🌵<LF><LF>للطلب والاستفسار تواصل واتساب مع د..سهام📲<LF>URL<LF>wtli",
"@USER لمن يعاني من السمنة والبدانة و الوزن الزائد<LF><LF>-يقضي على الترهلات والكرش<LF>كلين 9 لتخسيس الوزن💯<LF>-كلين9 يعمل على 'تخسيس وزنك من 10 إلى 15 كيلو <LF><LF>امن وفعال وصحي 100%<LF><LF>للطلب التواصل عالخاص<LF>URL<LF>rcydKv",
"@USER @USER 🎀♥♥♥♥💙👇👇👇👇👇👇👇👇 البديل الطبيعي للفياجرا <LF>لحل جميع المشكلات الجنسية 💚💚💚💛💛💛💘💘💘🌷🌷🌷💙💙❤❤👐👐👐👏👏👍👍👍<LF>💙♥♥💙♥💙<LF>🌹🌹🌹🌹<LF>👇👇F👇👇F👇F👇F👇<LF>URL<LF>x6b",
"عندك بحث ومو عارف تسويه ؟<LF>احنا نخدمك و نعملك بحث متكامل بأسعار رمزية<LF>تواصلوا خاص او واتس اب ٠٠٩٦٢٧٧٢٦٧٦٧٢٣ <LF>#بحوث #مشاريع_تخرج #جامعة #جامعة_الملك_فيصل  #جامعة_الطائف #جامعة_الشدادية #جامعة_الباحة  #جامعة_جدة #جامعه_القصيم #جامعة_الجوف #جامعة_الملك_عبدالعزيز #جامعه",
"@USER 🌹تخلص من مشاكل الحساسية والصدفيه والفطريات والقشور والجروح<LF><LF>و مشاكل القولون و الحموضه<LF>AA✅الافضل عالميا✅AA<LF><LF>♥️♥️✔✔✔⭕⭕<LF>♥♥👇👇👇 حيااكم احبائي و اصدقائي   حياة سعيدة بانتظاركم ان شاء الله 💛💛💘💘💘👐👏👏<LF>للطلب والاستفسار<LF>URL<LF>00p",
"@USER للعناية بالشعر وجماله والبشرة بشكل اصحي وامن تواصل عالخاص 😙😙<LF>URL",
"@USER لحظه صدق مع النفس ....مش بالضروى تكون نفس الصفات بس اكيد التلف اصاب بعض منها",
"RT @USER: الوقت ليل والشتاء بلا قمر <LF>نشتاق في سأم الشتاء شعاع دفء حولنا<LF>نشتاق قنديلا يسامر ليلنا ... نشتاق <LF>من يحكي لنا ..؟!<LF>نشتاق افرا…",
"RT @USER: اللهم إجعلنا ممن عفوت عنهم ، ورضيت عنهم ، وغفرت لهم ، وحميتهم من النار ، وكتبت لهم الجنة",
"RT @USER: صباح الخير، هل شخصياتنا في وسائل التواصل الاجتماعي مشابهة لما نحن عليه في الواقع؟",
"انطلاق تصفيات المرحلة الأولى<LF>من تصفيات #تحدي_القراءة_العربي<LF>التي تقام بــ #تعليم_بيشة<LF>في قطاعي البنين و البنات ضمن أنشطة الدورة الثالثة للمشروع . URL",
"الإنسان الأنيق في تعامله وحديثـه : يقتحـم أعماق كل من يقابله ويحظى بإحترام الجميع بطريقته كن بسيطًا تكن أجمل .! <LF><LF>#روز 🌸 URL",
"RT @USER: أصبحنا نتبسم لشاشة الأجهزه أكثر مما نتبسم في وجوه الناس<LF><LF>-<LF><LF>😴🌸🍃<LF>#آطيب_قلب ❤ URL",
"@USER وقضيتنا الكبرى في اكمال تعليمنا وحصولنا على البكالوريوس وتحسين اداءنا في مجال اختصاصنا",
"RT @USER: أشياءٌ كثِيرة لاَ تستحقُ منّا إلا أنْ نَنظُر لهَا بصمتْ لأن خُروج الكلماتْ حينهَا مُتعبٌ جداً",
"RT @USER: اللهم إن أبي كان باسمٌ الوجه، جميلُ الخلق، صابرًا في البلاء فأجعل مُستقره الجنة، ضاحكًا مستبشرًا يا أرحم الراحمين.",
]

var hateSamples = [
"#قطع_شريان_النسويات منشنوا الشريان ابو خدود على حساب نيزك عشان يشوف شلون هو غبي..",
"@atayyh مشروع الأنتقالي الجنوبي إستعادة الجنوب كاملاً ولن يتوقف حتى يطهر كل شبر من أرض الجنوب.",
"@nafeakleb2 الإمارات  صنعت الذي لم يلبيه ابن الجنوب عبدربه الاخونجي",
"اغلب الهمج الي داخله هنا تسب الشيعه هم مسوين نفسهم من سنتين ضد الصحوه و انها ضالمه و الحين مسوين نفسهم متفتحين و ال… https://t.co/bqjhfe0lIO",
"#طبيب_اجنبي_يتهجم_على_ممرضه NEWLINE طبعاً سلق الليبراليه والفسويات مالهم حس",
"شكرا نيزك على كشف النسويات وشلتهم #نيزك_يدار_من_تركيا",
"مستغربه من وضعكم، لا تصيرون مع إسقاط الولايه مانبي متخلفات بالله بس بطلوا تكونوا انانيات يا مريضات.",
"#فتاة_تايلاند تلك فَعْله لا تفعلها الحَرائِر  .",
"@Azoz30y @MasirahTV السياسة وما أدراك ما السياسة يظهرون خلاف مايبطنون حتى يخدعوا من استطاعوا..ابحث جيدا علاقات إيرا… https://t.co/3XV3P7CYDx",
"@jasemj67 قاتل الله الاخونج أينما كانوا ،يبيعون ضمائرهم من أجل مصلحهم.",
"@waleedalfarraj ياولد يالعيب الله الله شرقاوى يجرح ويداوى",
"﴿المُنافِقونَ وَالمُنافِقاتُ بَعضُهُم مِن بَعضٍ يَأمُرونَ بِالمُنكَرِ وَيَنهَونَ عَنِ المَعروفِ وَيَقبِضونَ أَيدِيَ… https://t.co/IlOD2drWF0",
"ابي احد يحبني يومين ويخونني عندي اغنيه عراقيه بنت كلب.",
"@MctMunicipality مرحباء اخواني هل يوجد أنابيب مياه تحت شارع مطرح  روي او عين مياه طبيعية",
"@RimmeAkram 😓😓😂😂😂🤦🤦🙆  NEWLINE هو حظنا كدة انا عارفه .. اول ما ملتقى حد حلو وذوق ومحترم وقلبنا تتعلق به يطلع مسيحى 🤦😭😭",
"الدوسري ظهير الهلال معار للرائد واهداف الهلال عن طريقه  NEWLINE احسن النيه 😂@TARIQALNOFAL   #الهلال_الرايد",
"مفروض ترند #العلاوه_النسويه12 #طبيب_اجنبي_يتهجم_علي_ممرضه",
"#لا_ولايه_علي_سفر_المراه NEWLINE  NEWLINE فعلك يدرّس يامحمد درااااااسة  NEWLINE ❤️❤️ https://t.co/XYSbrCFuDH",
"عنوان الأغنية مستوحى من سؤال طرحته مارجوري روزن في Popcorn Venus  خصته كدراسة نسوية عن ظهور النساء في هوليود و يعتب… https://t.co/vuyXt0EpJm",
"لكل من يقرا رسالتي الان❤️ ادعولي بظهر الغيب بان الله يجعل من احب من نصيبي وزوجا لي و الله يحقق لكم ما تتمنونه❤️… https://t.co/t3tRNfFfmh",
"RT @swed_hr: @politeabood @maryamabd97 @Ahmad94278657 تقول بالعام ذلتنا وبالخاص تترجاك الاعتذار",
]

// function upload(){

//   var data=new FormData();
//           var file = $("#fileupload")[0].files[0];
//           if (typeof file == "undefined"){
//             alert ("Please choose file.");
//             return;
//           }
//           data.append('file',file);
//           $("#txtTest").val("Classifier training in progress. Please wait.....");

//           $.ajax({
//               url:"/upload",
//               type:'POST',
//               data:data,
//               cache:false,
//               processData:false,
//               contentType:false,
//               error:function(){
//                   alert ("Upload error");
//                   console.log("upload error");
//               },
//               success:function(data){
//                   console.log(data);
//                   $("#txtTest").val("Classifier training complete. Your classifier will be used for violence detection.");
//               }
//           })
// }

function clear_table(){
  $("#pie-chart").hide();
  $("#pie-chart2").hide();
  
  $("#indTable").hide();
  $('#indTable2').hide();
  $('#indTable3').hide();
  $("#indTable4").hide();
  $('#indTable5').hide();
  $('#indTable6').hide();
  $("#indTable7").hide();
  $('#indTable8').hide();
  $('#indTable9').hide();



  $("#info1").hide();
  $("#info2").hide();
  $("#info3").hide();
  $("#info4").hide();
  $("#info5").hide();
  $("#info6").hide();

  $("table tbody").html('');
  console.log("hallo");
}




/**
Gets input from user, makes call to server and updates DOM based on level of 
offensivebess in text input by user as returned from server.
**/
function query_offense() {


  // gets input from user
  var classifier = $('#classifiername').find(":selected").text();
  var text = $('#search').val();

  if (text.length < 1){
    alert ("Empty text. Please enter text.");
    return
  }
  $('html, body').css("cursor", "wait");
  $(".processing").show();


  // makes request to server and updates dom
  $.post('/queryOffense', {
      text: text,
      model: classifier,
  }).done(function(response) {
      console.log(response);
      $('#indTable3').hide();
      $("#indTable").show();
      $('#indTable2').show();
      $("#indTable table tbody").html("");
      $("#indTable2 table tbody").html("");
      $("#indTable3 table tbody").html("");


      var levels = response['levels'];
      var level = '';
      var text = '';
      var count1 = 0;
      var count2 = 0;
      var tweets = response['tweets'];
      console.log(level);
      for (var i = 0; i < levels.length; i++){
        level = levels[i];
        text = tweets[i];
        if (level == "NOT"){
          count1 += 1;
          var markup = "<tr><td><strong> <font color = 'blue'>" + text + "</td><td> </font> <font color = 'blue'> <strong> not offensive </font> </strong> </td></tr>";
          $("#indTable2 table tbody").append(markup);
        }

        else {
          count2 += 1;
          var markup = "<tr><td> <strong><font color = 'red'>" + text + "</td><td> </font> <font color = 'red'> <strong> offensive </font> </strong></td></tr>";
          $("#indTable table tbody").append(markup);
        }
      }

      $("#info1").html("Found <strong>" + count2.toString() + "</strong> offensive tweets out of <strong>" + (count1 + count2).toString() + "</strong> tweets.");
      $("#info2").html("Found <strong>" + count1.toString() + "</strong> non offensive tweets out of <strong>" + (count1 + count2).toString() +  "</strong> tweets.");

      $("#info1").show();
      $("#info2").show();

      pieChart.data.datasets[0].data = [count2, count1]
      pieChart.update();
      $("#pie-chart").show();
      $(".processing").hide();


      $('html, body').css("cursor", "auto");




  }).fail(function() {
      alert("Server error");
      $('html, body').css("cursor", "auto");
      $(".processing").hide();


  });
  
} 


/**
Gets input from user, makes call to server and updates DOM based on level of 
offensivebess in text input by user as returned from server.
**/
function detect_offense() {

  $("#pie-chart").hide();

  // gets input from user
  var classifier = $('#classifiername').find(":selected").text();
  var text = $('#search').val();

  if (text.length < 1){
    alert ("Empty text. Please enter text.");
    return
  }

  // makes request to server and updates dom
  $.post('/detectOffense', {
      text: text,
      model: classifier,
  }).done(function(response) {
      $("#info1").hide();
      $("#info2").hide();
      $("#indTable").hide();
      $('#indTable2').hide();
      $('#indTable3').show();

      var level = response['level']
      console.log(level);
      if (level == "NOT"){
        var markup = "<tr><td><strong> <font color = 'blue'>" + text + "</td><td> </font> <font color = 'blue'> <strong> not offensive </font> </strong> </td></tr>";
        $("#indTable3 table tbody").append(markup);
      }

      else {
        var markup = "<tr><td> <strong><font color = 'red'>" + text + "</td><td> </font> <font color = 'red'> <strong> offensive </font> </strong></td></tr>";
        $("#indTable3 table tbody").append(markup);
      }

  }).fail(function() {
      alert("Server error");
  });
  
} 

function query_ad(){
  // gets input from user
  var classifier = $('#classifiername2').find(":selected").text();
  var text = $('#search2').val();

  if (text.length < 1){
    alert ("Empty text. Please enter text.");
    return
  }

  $('html, body').css("cursor", "wait");
  $(".processing").show();


  // makes request to server and updates dom
  $.post('/queryAd', {
      text: text,
      model: classifier,
  }).done(function(response) {
      console.log(response);
      $('#indTable6').hide();
      $("#indTable4").show();
      $('#indTable5').show();

      $("#indTable4 table tbody").html("");
      $("#indTable5 table tbody").html("");
      $("#indTable6 table tbody").html("");
      var levels = response['levels'];
      var level = '';
      var text = '';
      var count1 = 0;
      var count2 = 0;
      var tweets = response['tweets'];
      console.log(level);
      for (var i = 0; i < levels.length; i++){
        level = levels[i];
        text = tweets[i];
        if (level == "__label__NOTADS"){
          count1 += 1;
          var markup = "<tr><td><strong> <font color = 'blue'>" + text + "</td><td> </font> <font color = 'blue'> <strong> not advertisement </font> </strong> </td></tr>";
          $("#indTable5 table tbody").append(markup);
        }

        else {
          count2 += 1;
          var markup = "<tr><td> <strong><font color = 'red'>" + text + "</td><td> </font> <font color = 'red'> <strong> advertisement </font> </strong></td></tr>";
          $("#indTable4 table tbody").append(markup);
        }
      }

      $("#info3").html("Found <strong>" + count2.toString() + "</strong> advertisement tweets out of <strong>" + (count1 + count2).toString() + "</strong> tweets.");
      $("#info4").html("Found <strong>" + count1.toString() + "</strong> non advertisement tweets out of <strong>" + (count1 + count2).toString() +  "</strong> tweets.");

      $("#info3").show();
      $("#info4").show();


      pieChart2.data.datasets[0].data = [count2, count1]
      pieChart2.update();
      $("#pie-chart2").show();

      $('html, body').css("cursor", "auto");
      $(".processing").hide();




  }).fail(function() {
      alert("Server error");
      $('html, body').css("cursor", "auto");
      $(".processing").hide();


  });
  
}


/**
Gets input from user, makes call to server and updates DOM based on level of 
offensivebess in text input by user as returned from server.
**/
function detect_ad() {
  $("#pie-chart2").hide();

  // gets input from user
  var classifier = $('#classifiername2').find(":selected").text();
  var text = $('#search2').val();

  if (text.length < 1){
    alert ("Empty text. Please enter text.");
    return
  }

  // makes request to server and updates dom
  $.post('/detectAd', {
      text: text,
      model: classifier,
  }).done(function(response) {
      $("#info3").hide();
      $("#info4").hide();
      $("#indTable4").hide();
      $('#indTable5').hide();
      $('#indTable6').show();
      var level = response['level']
      console.log(level);

      if (level == "__label__NOTADS"){
        var markup = "<tr><td><strong> <font color = 'blue'>" + text + "</td><td> </font> <font color = 'blue'> <strong> not advertisement </font> </strong> </td></tr>";
        $("#indTable6 table tbody").append(markup);
      }

      else {
        var markup = "<tr><td> <strong><font color = 'red'>" + text + "</td><td> </font> <font color = 'red'> <strong> advertisement </font> </strong></td></tr>";
        $("#indTable6 table tbody").append(markup);
      }

  }).fail(function() {
      alert("Server error");
  });
  
} 


function query_hate(){
  // gets input from user
  var classifier = $('#classifiername3').find(":selected").text();
  var text = $('#search3').val();

  if (text.length < 1){
    alert ("Empty text. Please enter text.");
    return
  }

  $('html, body').css("cursor", "wait");
  $(".processing").show();


  // makes request to server and updates dom
  $.post('/queryHate', {
      text: text,
      model: classifier,
  }).done(function(response) {
      console.log(response);
      $('#indTable9').hide();
      $("#indTable7").show();
      $('#indTable8').show();

      $("#indTable7 table tbody").html("");
      $("#indTable8 table tbody").html("");
      $("#indTable9 table tbody").html("");
      var levels = response['levels'];
      var level = '';
      var text = '';
      var count1 = 0;
      var count2 = 0;
      var tweets = response['tweets'];
      console.log(level);
      for (var i = 0; i < levels.length; i++){
        level = levels[i];
        text = tweets[i];
        if (level == "NOT_HS"){
          count1 += 1;
          var markup = "<tr><td><strong> <font color = 'blue'>" + text + "</td><td> </font> <font color = 'blue'> <strong> not hate-speech </font> </strong> </td></tr>";
          $("#indTable8 table tbody").append(markup);
        }

        else {
          count2 += 1;
          var markup = "<tr><td> <strong><font color = 'red'>" + text + "</td><td> </font> <font color = 'red'> <strong> hate-speech </font> </strong></td></tr>";
          $("#indTable7 table tbody").append(markup);
        }
      }

      $("#info5").html("Found <strong>" + count2.toString() + "</strong> hate-speech tweets out of <strong>" + (count1 + count2).toString() + "</strong> tweets.");
      $("#info6").html("Found <strong>" + count1.toString() + "</strong> not hate-speech tweets out of <strong>" + (count1 + count2).toString() +  "</strong> tweets.");

      $("#info5").show();
      $("#info6").show();


      pieChart3.data.datasets[0].data = [count2, count1]
      pieChart3.update();
      $("#pie-chart3").show();

      $('html, body').css("cursor", "auto");
      $(".processing").hide();




  }).fail(function() {
      alert("Server error");
      $('html, body').css("cursor", "auto");
      $(".processing").hide();


  });
  
}


/**
Gets input from user, makes call to server and updates DOM based on 
hate-speech in text input by user as returned from server.
**/
function detect_hate() {
  $("#pie-chart3").hide();

  // gets input from user
  var classifier = $('#classifiername3').find(":selected").text();
  var text = $('#search3').val();

  if (text.length < 1){
    alert ("Empty text. Please enter text.");
    return
  }

  // makes request to server and updates dom
  $.post('/detectHate', {
      text: text,
      model: classifier,
  }).done(function(response) {
      $("#info5").hide();
      $("#info6").hide();
      $("#indTable7").hide();
      $('#indTable8').hide();
      $('#indTable9').show();
      var level = response['level']
      console.log(level);

      if (level == "NOT_HS"){
        var markup = "<tr><td><strong> <font color = 'blue'>" + text + "</td><td> </font> <font color = 'blue'> <strong> not hate-speech </font> </strong> </td></tr>";
        $("#indTable9 table tbody").append(markup);
      }

      else {
        var markup = "<tr><td> <strong><font color = 'red'>" + text + "</td><td> </font> <font color = 'red'> <strong> hate-speech </font> </strong></td></tr>";
        $("#indTable9 table tbody").append(markup);
      }

  }).fail(function() {
      alert("Server error");
  });
  
}


// gets random input for offense detection
function randomizeOff() {
  if (document.getElementById('searchType').checked){
    console.log ("GOTCHU");
    var rand = queries[Math.floor(Math.random() * queries.length)];
    document.getElementById("search").value = rand;
  } else {
    console.log("I WEEP");
    var rand = offensiveSamples[Math.floor(Math.random() * offensiveSamples.length)];
    document.getElementById("search").value = rand;
  }
}

// gets random input for ad detection
function randomizeAd() {
  if (document.getElementById('searchType2').checked){
    console.log ("GOTCHU");
    var rand = queries[Math.floor(Math.random() * queries.length)];
    document.getElementById("search2").value = rand;
  } else {
    console.log("I WEEP");
    var rand = adSamples[Math.floor(Math.random() * adSamples.length)];
    document.getElementById("search2").value = rand;
  }
}

// gets random input for hate-speech detection
function randomizeHate() {
  if (document.getElementById('searchType3').checked){
    console.log ("GOTCHU");
    var rand = queries[Math.floor(Math.random() * queries.length)];
    document.getElementById("search3").value = rand;
  } else {
    console.log("I WEEP");
    var rand = hateSamples[Math.floor(Math.random() * hateSamples.length)];
    document.getElementById("search3").value = rand;
  }
}

// checks if user wants to analyze text or make a query. redirects request accordingly
function check_offense(){
  if (document.getElementById('searchType').checked){
    query_offense();
  } else {
    detect_offense();
  }
}

// checks if user wants to analyze text or make a query. redirects request accordingly
function check_ad(){
  if (document.getElementById('searchType2').checked){
    query_ad();
  } else {
    detect_ad();
  }
}



function check_hate(){
  if (document.getElementById('searchType3').checked){
    query_hate();
  } else {
    detect_hate();
  }
}