Vue.createApp({
  delimiters:["${","}"],
  methods:{
    onclick(tab){
      this.current = tab;
    }
  },
  computed:{
    // タブ名の取得
    tabNames(){
      return Object.keys(this.tabs);
    },
    currentTab(){
      return `tab-${this.current}`;
    }
  },
  data(){
    return{
      current:'result',
      tabs:{
        'result':'診断結果',
        'topic':'タイプの特徴',
      }
    }
  }

})
.component('tab-result',{
  delimiters:["{{","}}"],
  name: 'tab-result',
  // template: `<div class="tab">おはよう</div>`,
  template: `<div class="tab">
            <div class="bar-graph-wrap">
            <div>おはようございます</div>
            {% for result in result_data %}
            <div class="graph" style="width: {{ result }}%;">
                <span class="name">タイプ{{ forloop.counter }}</span>
                <span class="number">{{ result }}</span>
            </div>
            {% endfor %}
            </div>
            </div>`,
  data(){
    return{
      name:''
    }
  }
})
.component('tab-topic',{
  delimiters:["${","}"],
  name: 'tab-topic',
  template: `<div class="tab">こんにちは
  </div>`,
  data(){
    return{
      name:''
    }
  }
})
.mount('#app')