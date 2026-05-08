# じしゃくの もよう · Jishaku no Moyō — Magnet Patterns

> **見えない『力のかたち』が、すがたを あらわす。**
> The invisible "shape of force" suddenly appears.

5〜9さい むけ、ブラウザで動く **磁場（じば）の あそびば**。
画面いっぱいの **600つぶの 鉄粉（てっぷん）** が、ほんもののように 磁場の むきに そろって ならぶ。じしゃくを ゆびで うごかすと、もよう ぜんたい が ゆれて、組みなおされる。

A browser-based **iron-filings sandbox** for kids ages 5–9. ~600 simulated filings cover the screen and orient themselves to the local magnetic field, just like the real thing. Drag the magnet and the whole pattern rearranges in real time.

▶ **[Play in browser](https://pndshch.github.io/jishaku-moyo/)**

## なに が できるの？ / What can you do?

- **1じしゃく** — ぼう型 じしゃく の まわりに ひろがる、教科書 そのままの **ダイポール 磁場**。
- **2じしゃく** — タップで N⇄S 反転。**同じ極** は しりぞけあい、**ちがう極** は 引きあう。じっさいに もよう が ぜんぜん ちがう。
- **U字（馬蹄）** — N と S が 近い ぶん、すき間に **力 が ぎゅっと あつまる**。クレーン・スピーカー・電気モーターの しくみ。
- **線モード** — 鉄粉の あと が のこって、**磁力線（じりょくせん）** が えがかれる。
- **JP / EN** バイリンガル。

## なぜ 作ったか / Why

子ども向けの 物理アプリ は、「光」や「音」は たくさん あるのに、「**磁石の 力**」 を じっさいに 触れる ものは ほとんど ない。
鉄粉 を まいて 磁石の もよう を 見る あの たいけん は、安全 と 後始末 の 都合で、いまの 子ども は ほとんど できなくなった。
ブラウザ なら、何度でも、安全に、まっさらな 紙を ばらまける。

Few kids today get to sprinkle real iron filings — too messy, too hazardous. The browser version is safe, infinite, and undoable.

## つくり / How it works

各 鉄粉 は 各フレーム で:
1. すべての 磁極 から の 場ベクトル を たし合わせる（クーロン的 1/r² モデル、近距離 ソフトクランプ）
2. その むき に 32% ずつ 回転 する（180度対称：線分なので ±π を 同一視）
3. 場の 強さ を 線の 長さ・濃さ に 反映

Per frame, each filing sums the field vectors from all magnetic poles (Coulomb-like 1/r² with a soft minimum), interpolates 32 % toward the target angle (with 180°-symmetric shortest-rotation, since filings are line segments, not arrows), and uses field magnitude to set length and opacity.

1 まい HTML, ライブラリ なし, データ は のこさない. Single HTML file, no libraries, no data stored.

---

Pinda Lab · 2026
