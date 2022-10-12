Vue.createApp({
  created() {
    this.interval = setInterval(() => {
      this.current_slide = (this.current_slide + 1) % this.slides.length;
    },3000
    );
  },
  // methods: {
    
  // },
  // アプリ中に使うデータの定義
  data() {
    return{
      Active: false,
      current_slide: 0,
      // フォルダはテンプレートから見てのもの
      slides: [{img:'./static/account/img/slider_01.png'},
               {img:'./static/account/img/slider_02.png'},
               {img:'./static/account/img/slider_03.png'},

              ],
    }
  },
}).mount('#slider');
