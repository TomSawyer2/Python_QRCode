(self["webpackChunkpython_qrcode_web"]=self["webpackChunkpython_qrcode_web"]||[]).push([[512],{91927:function(e,a,s){"use strict";s.r(a),s.d(a,{default:function(){return P}});s(99437);var r=s(86792),n=(s(36044),s(70147)),t=(s(51366),s(59813)),c=(s(71270),s(51494)),i=(s(83044),s(76974)),l=(s(14352),s(61853)),o=(s(70779),s(3953)),d=s(57113),u=(s(94707),s(2408)),p=s(82005),x=s(71188),h=s(50959),m=s(11527),v=()=>(0,m.jsx)("div",{className:"navbar",children:(0,m.jsx)("div",{className:"navbar-box",children:(0,m.jsx)("span",{className:"navbar-title",children:"Python_QRCode WebUI"})})}),j=v,f=s(46090),b=s.n(f),Z=[200],g={timeout:1e5,headers:{"Content-type":"application/json"},baseURL:"http://127.0.0.1:5000"},N=e=>{var a=e.status,s=e.data;if(!Z.includes(a)||0!==s.code)throw s.message;return s},w=e=>{var a,s=e.response;throw null!==s&&void 0!==s&&null!==(a=s.data)&&void 0!==a&&a.message?s.data.message:e},k=b().create(g);k.interceptors.response.use(N,w);var y=k;function C(e){return S.apply(this,arguments)}function S(){return S=(0,p.Z)((0,d.Z)().mark((function e(a){var s,r,n;return(0,d.Z)().wrap((function(e){while(1)switch(e.prev=e.next){case 0:return s="/api/encode",e.next=3,y.post(s,a);case 3:return r=e.sent,n=r.data,e.abrupt("return",n);case 6:case"end":return e.stop()}}),e)}))),S.apply(this,arguments)}function R(e){return q.apply(this,arguments)}function q(){return q=(0,p.Z)((0,d.Z)().mark((function e(a){var s,r,n;return(0,d.Z)().wrap((function(e){while(1)switch(e.prev=e.next){case 0:return s="/api/decode",e.next=3,y.post(s,a);case 3:return r=e.sent,n=r.data,e.abrupt("return",n);case 6:case"end":return e.stop()}}),e)}))),q.apply(this,arguments)}var U=(e,a)=>{var s=document.createElement("a");s.href=e,s.download=a,s.click()},_=(s(5997),s(19041)),A=s(88106),D=e=>{var a=e.color,s=e.onChange;return(0,m.jsx)(_.Z,{content:(0,m.jsx)(A.AI,{color:a,onChangeComplete:e=>s(e.hex)}),children:(0,m.jsx)("div",{className:"color-circle",style:{backgroundColor:a}})})},I=D,L=()=>{var e=(0,h.useState)(""),a=(0,x.Z)(e,2),s=a[0],v=a[1],f=(0,h.useState)(""),b=(0,x.Z)(f,2),Z=b[0],g=b[1],N=(0,h.useState)(!1),w=(0,x.Z)(N,2),k=w[0],y=w[1],S=(0,h.useState)(""),q=(0,x.Z)(S,2),_=q[0],A=q[1],D=(0,h.useState)(""),L=(0,x.Z)(D,2),P=L[0],z=L[1],G=(0,h.useState)(!1),T=(0,x.Z)(G,2),B=T[0],E=T[1],F=(0,h.useState)("#ffffff"),J=(0,x.Z)(F,2),M=J[0],Q=J[1],W=(0,h.useState)("#000000"),Y=(0,x.Z)(W,2),H=Y[0],K=Y[1],O=function(){var e=(0,p.Z)((0,d.Z)().mark((function e(a){var s,r,n,t,c;return(0,d.Z)().wrap((function(e){while(1)switch(e.prev=e.next){case 0:if(s="image/jpeg"===a.type,r="image/png"===a.type,s||r){e.next=5;break}return u.default.error("You can only upload JPG/PNG file!"),e.abrupt("return",!1);case 5:if(n=a.size/1024/1024<5,n){e.next=9;break}return u.default.error("Image must smaller than 2MB!"),e.abrupt("return",!1);case 9:t="",c=new FileReader,c.readAsDataURL(a),c.onload=(0,p.Z)((0,d.Z)().mark((function e(){var a;return(0,d.Z)().wrap((function(e){while(1)switch(e.prev=e.next){case 0:return a=c.result,t=a.replace("data:image/png;base64,",""),A(t),e.abrupt("return",!1);case 4:case"end":return e.stop()}}),e)})));case 13:case"end":return e.stop()}}),e)})));return function(a){return e.apply(this,arguments)}}(),V=function(){var e=(0,p.Z)((0,d.Z)().mark((function e(){var a;return(0,d.Z)().wrap((function(e){while(1)switch(e.prev=e.next){case 0:return y(!0),e.prev=1,e.next=4,C({data:s,backColor:M,fillColor:H});case 4:a=e.sent,g("data:image/png;base64,".concat(a)),u.default.success("\u751f\u6210\u6210\u529f"),e.next=12;break;case 9:e.prev=9,e.t0=e["catch"](1),console.error(e.t0);case 12:y(!1);case 13:case"end":return e.stop()}}),e,null,[[1,9]])})));return function(){return e.apply(this,arguments)}}(),X=function(){var e=(0,p.Z)((0,d.Z)().mark((function e(){var a;return(0,d.Z)().wrap((function(e){while(1)switch(e.prev=e.next){case 0:if(_){e.next=2;break}return e.abrupt("return");case 2:return E(!0),e.prev=3,e.next=6,R({data:_});case 6:a=e.sent,z(null===a||void 0===a?void 0:a[0]),u.default.success("\u89e3\u7801\u6210\u529f"),e.next=14;break;case 11:e.prev=11,e.t0=e["catch"](3),console.error(e.t0);case 14:E(!1);case 15:case"end":return e.stop()}}),e,null,[[3,11]])})));return function(){return e.apply(this,arguments)}}(),$=()=>{var e="output-".concat((new Date).getTime(),".png");U(Z,e)};return(0,m.jsxs)("div",{className:"container",children:[(0,m.jsx)(j,{}),(0,m.jsxs)(r.Z,{className:"qr",children:[(0,m.jsx)(c.Z,{className:"qr-card",span:8,children:(0,m.jsxs)("div",{className:"encode",children:[(0,m.jsx)(o.Z.TextArea,{rows:4,allowClear:!0,className:"encode-input",placeholder:"\u8bf7\u8f93\u5165\u8981\u7f16\u7801\u7684\u5185\u5bb9",autoSize:{minRows:4,maxRows:4},onChange:e=>v(e.target.value)}),(0,m.jsxs)("div",{className:"color-group",children:[(0,m.jsxs)("div",{className:"color-box",children:[(0,m.jsx)("span",{children:"\u80cc\u666f\u8272"}),(0,m.jsx)(I,{color:M,onChange:e=>Q(e)})]}),(0,m.jsxs)("div",{className:"color-box",children:[(0,m.jsx)("span",{children:"\u586b\u5145\u8272"}),(0,m.jsx)(I,{color:H,onChange:e=>K(e)})]})]}),(0,m.jsx)("div",{className:"encode-img",children:""===Z?(0,m.jsx)("div",{className:"empty-img-box",children:k&&(0,m.jsx)(l.Z,{})}):(0,m.jsx)("div",{className:"img-box",children:k?(0,m.jsx)(l.Z,{}):(0,m.jsx)("img",{className:"image",src:Z})})}),(0,m.jsxs)("div",{children:[(0,m.jsx)(i.Z,{className:"encode-btn",onClick:()=>V(),disabled:""===s||k,children:(0,m.jsx)("span",{className:"encode-btn-text",children:"\u751f\u6210"})}),(0,m.jsx)(i.Z,{type:"primary",className:"encode-btn",onClick:()=>$(),disabled:""===s||k,children:(0,m.jsx)("span",{className:"encode-btn-text",children:"\u4fdd\u5b58"})})]})]})}),(0,m.jsx)(c.Z,{className:"qr-card",span:8,children:(0,m.jsxs)("div",{className:"decode",children:[(0,m.jsx)("div",{className:"decode-img",children:(0,m.jsx)(t.Z.Dragger,{showUploadList:!1,beforeUpload:O,children:(0,m.jsx)("div",{className:"img-box",children:""===_?(0,m.jsx)("div",{className:"empty-img-box-upload"}):(0,m.jsxs)("div",{className:"mask-box",children:[(0,m.jsx)("img",{className:"image",src:"data:image/png;base64,".concat(_)}),(0,m.jsx)("div",{className:"mask",children:(0,m.jsx)(i.Z,{children:"\u66f4\u65b0"})})]})})})}),(0,m.jsx)("div",{className:"decode-output",children:B?(0,m.jsx)(l.Z,{}):(0,m.jsx)(n.Z,{placement:"top",title:P,children:(0,m.jsx)("span",{className:"output-text",children:P})})}),(0,m.jsx)(i.Z,{type:"primary",className:"decode-btn",onClick:()=>X(),children:(0,m.jsx)("span",{className:"decode-btn-text",children:"\u8bc6\u522b"})})]})})]}),(0,m.jsx)("div",{className:"bg"})]})},P=L}}]);