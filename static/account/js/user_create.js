Vue.createApp({
  delimiters: [
    "${","}"
  ],
  methods: {
    onclick(tab){
      // 表示タブの制御
      this.current = tab;
      this.labels = this.items[this.current];
    }
  },
  // タブ名の取得
  computed:{
    // タブのキー配列
    tabNames(){
      return Object.keys(this.tabs);
    }
  },
  // アプリ中に使うデータの定義
  data() {
    return{
      current: 'must',
      tabs: {
        'must':'必須項目',
        'any':'任意項目'
      },
      items:{
        'must':['メールアドレス','パスワード','パスワード(確認用)'],
        'any':['苗字','名前','職業']
      },
      // labels: this.items[this.current],
      labels: ['メールアドレス','パスワード','パスワード(確認用)'],
    }
  },
})
.mount('#login-form');

// .component('must',{
//   name: 'must',
//   template:`
//   `,

// }
// )