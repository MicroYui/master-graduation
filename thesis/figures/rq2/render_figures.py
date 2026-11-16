"""Redraw the final EviComRL experiment values with thesis typography.

Requires matplotlib, numpy, and suitable Chinese/Latin fonts. Bundled source_data
files are used first; an optional external study directory only fills missing
files. This script does not run training or change experimental values.
"""
from pathlib import Path
import argparse
import csv
import json
import shutil
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--study", type=Path,
    default=HERE.parents[2] / "graduation_second_question" / "outputs/rq_suite/fixed5_v2_features_20260715_152059",
    help="External completed study used only to fill missing source_data files.")
parser.add_argument("--figures", nargs="+", choices=["main_accuracy", "quality_cost", "training_curve",
    "agent_count", "budget", "max_steps", "link_profile", "message_modes", "trace_scale", "ablation", "reliability"],
    help="Only save these figures; by default all 11 figures are saved.")
args = parser.parse_args()
STUDY = args.study.expanduser().resolve()
DATA = HERE / "source_data"
DATA.mkdir(exist_ok=True)
rendered = []
fonts = {f.name for f in font_manager.fontManager.ttflist}
cjk = next((f for f in ["SimSun", "SimSong", "Songti SC", "Noto Serif CJK SC"] if f in fonts), "DejaVu Sans")
plt.rcParams.update({"font.family": ["Times New Roman", cjk], "font.size": 9,
    "axes.labelsize": 9, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "legend.fontsize": 8, "axes.unicode_minus": False, "pdf.fonttype": 3,
    "savefig.dpi": 300, "axes.spines.top": False, "axes.spines.right": False})
BLUE, GRAY = "#244e7a", "#a5b3c2"

def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def source_file(name, external_path):
    """Keep packaged results authoritative; copy an external file only if absent."""
    local_path = DATA / name
    if local_path.is_file():
        return local_path
    if not external_path.is_file():
        raise FileNotFoundError(
            f"Missing bundled data {local_path}; external fallback also absent: "
            f"{external_path}. Restore source_data or provide --study.")
    shutil.copyfile(external_path, local_path)
    return local_path

def save(fig, name):
    if args.figures and name not in args.figures:
        plt.close(fig)
        return
    for ext in ["pdf", "png"]:
        fig.savefig(HERE / f"{name}.{ext}", bbox_inches="tight", pad_inches=.035)
    plt.close(fig)
    rendered.append(name)

def clean(ax):
    ax.grid(axis="y", color=".85", linewidth=.5)
    ax.set_axisbelow(True)

main_source = source_file("main_methods.csv", STUDY / "main/default/tables/method_comparison.csv")
main = rows(main_source)
calibrated = next(r for r in main if r["method"] == "EviComRL-w/oDeliveryDiscount")
default = next(r for r in main if r["method"] == "EviComRL")
main = [dict(r) for r in main if r["method"] not in {"OracleGreedy", "EviComRL-w/oDeliveryDiscount"}]
for r in main:
    r["method"] = {"EviComRL-MLP": "PPO-MLP", "Where2Comm": "Where2Comm-Trace", "How2Comm": "How2Comm-Trace"}.get(r["method"], r["method"])
main.sort(key=lambda r: float(r["accuracy"]))
fig, ax = plt.subplots(figsize=(6.45, 3.55), layout="constrained")
ax.barh([r["method"] for r in main], [100*float(r["accuracy"]) for r in main], color=[BLUE if r["method"] == "EviComRL" else GRAY for r in main], height=.67)
for i, r in enumerate(main):
    ax.text(100*float(r["accuracy"])+.6, i, f'{100*float(r["accuracy"]):.2f}', va="center", fontsize=8)
ax.set_xlim(0, 64)
ax.set_xlabel("准确率 / %")
ax.grid(axis="x", color=".87", linewidth=.5)
ax.set_axisbelow(True)
save(fig, "main_accuracy")

fig, ax = plt.subplots(figsize=(6.45, 2.50))
fig.subplots_adjust(left=.09, right=.66, bottom=.20, top=.96)
ordered = sorted(main, key=lambda r: -float(r["effective_quality"]))
for i, r in enumerate(ordered):
    x,y = float(r["avg_tokens"]),float(r["effective_quality"])
    ax.scatter(x,y, color=BLUE if i==0 else GRAY, marker="*" if i==0 else "o", s=85 if i==0 else 28, edgecolors=".25", linewidths=.4, label=f'{i+1}. {r["method"]}')
    offsets = {0:(4,5),1:(3,-11),2:(4,5),3:(4,6),4:(4,6),5:(4,5),6:(-12,2),7:(-16,4),8:(5,1),9:(5,-10),10:(4,-7),11:(4,-4)}
    ax.annotate(str(i+1),(x,y),textcoords="offset points",xytext=offsets.get(i,(3,4)),fontsize=8)
ax.set(xlabel="每任务平均通信量 / token", ylabel="有效信念质量", xlim=(-3,91), ylim=(.18,.43))
clean(ax)
ax.legend(loc="upper left", bbox_to_anchor=(1.02,1), frameon=False,
    handletextpad=.3, borderaxespad=0, labelspacing=.32, fontsize=7.6)
save(fig,"quality_cost")

history_path=source_file("rl_history.json", STUDY/"main/default/metrics/rl_history.json")
hist=json.loads(history_path.read_text())["0"]
fig,ax=plt.subplots(figsize=(6.45,2.55),layout="constrained")
ax.plot(range(1,len(hist)+1),hist,color=BLUE,lw=1.3)
ax.set(xlabel="训练轮次",ylabel="平均回合回报",xlim=(1,len(hist)))
clean(ax)
save(fig,"training_curve")

metrics=[("accuracy","准确率"),("balanced_accuracy","平衡准确率"),("effective_quality","有效信念质量"),("avg_tokens","每任务平均通信量 / token")]
groups=[
    ("agent_count",["agents_3","agents_6","agents_9"],[3,6,9],"局部视角数量",None),
    ("budget",["t60","t120","t180","t240"],[60,120,180,240],"通信预算 / token",None),
    ("max_steps",["steps_4","steps_8","steps_12"],[4,8,12],"最大通信步数",None),
    ("link_profile",["easy","medium","hard"],[0,1,2],"链路条件",["良好","中等","较差"]),
    ("message_modes",["label_only","label_claim","label_claim_summary","all_modes"],[1,2,3,4],"消息模式集合",["标签","+陈述","+摘要","全部"]),
    ("trace_scale",["n500","n1000","n2000"],[500,1000,2000],"语义轨迹数量",None),
]
styles=[("EviComRL","EviComRL",BLUE,"o"),("EviComRL-MLP","PPO-MLP","#65727c","s"),("ContextualBandit","ContextualBandit","#ad7742","^"),("FullComm","FullComm","#677f61","D")]
for group,conditions,xvals,xlabel,xticklabels in groups:
    series=[]
    for cond in conditions:
        source=source_file(f"{group}_{cond}.csv", STUDY/group/cond/"tables/method_comparison.csv")
        series.append(rows(source))
    # The three comparisons in the thesis share a compact two-row layout.
    # Keep every curve and data point; change geometry rather than stretching.
    compact = group in {"agent_count", "budget", "link_profile"}
    fig,axs=plt.subplots(2,2,figsize=(6.45,3.30 if compact else 4.5),layout="constrained")
    if compact:
        fig.get_layout_engine().set(w_pad=.025, h_pad=.025, wspace=.04, hspace=.04)
    for i,(key,label) in enumerate(metrics):
        ax=axs.flat[i]
        for method,display,color,marker in styles:
            ys=[float(next(r for r in block if r["method"]==method)[key]) for block in series]
            ax.plot(xvals,ys,marker=marker,color=color,lw=1.3,ms=3.5,label=display)
        ylabel = "平均通信量 / token" if compact and key=="avg_tokens" else label
        ax.set(xlabel=xlabel if not compact or i>=2 else "",ylabel=ylabel,xticks=xvals)
        if compact:
            ax.tick_params(axis="both", pad=2)
        if xticklabels: ax.set_xticklabels(xticklabels)
        clean(ax)
    handles,labels=axs[0,0].get_legend_handles_labels()
    fig.legend(handles,labels,loc="outside upper center",ncol=4,frameon=False)
    save(fig,group)

ablation_names=[("default","基准设置"),("wo_blind_center","取消盲中心"),("wo_center_bonus","取消中心偏好"),("wo_drop_risk_reward","取消风险代价"),("wo_link_aware_score","取消链路排序"),("wo_rerank","取消重排序"),("wo_token_cost_reward","取消长度代价"),("wo_warm_start","取消预热")]
ablation=[dict(default,display="基准设置")]
for cond,label in ablation_names[1:]:
    source=source_file(f"ablation_{cond}.csv", STUDY/"ablation"/cond/"tables/method_comparison.csv")
    ablation.append(dict(next(r for r in rows(source) if r["method"]=="EviComRL"),display=label))
fig,axs=plt.subplots(2,2,figsize=(6.45,5.85),layout="constrained")
for ax,(key,label) in zip(axs.flat,[("balanced_accuracy","平衡准确率"),("macro_f1","宏平均 F1"),("effective_quality","有效信念质量"),("avg_tokens","每任务平均通信量 / token")]):
    display=list(reversed(ablation))
    vals=[float(r[key]) for r in display]
    ax.barh([r["display"] for r in display],vals,color=[BLUE if r["display"]=="基准设置" else GRAY for r in display],height=.66)
    for i,v in enumerate(vals): ax.text(v+(.005 if key!="avg_tokens" else .5),i,f"{v:.3f}" if key!="avg_tokens" else f"{v:.1f}",va="center",fontsize=7)
    ax.set_xlabel(label)
    ax.set_xlim(0,(.66 if key!="avg_tokens" else 67))
    ax.grid(axis="x",color=".87",lw=.5)
    ax.set_axisbelow(True)
save(fig,"ablation")

if not args.figures or "ablation" in args.figures:
    with (DATA/"ablation_summary.csv").open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,lineterminator="\n",fieldnames=["display", "accuracy", "balanced_accuracy", "macro_f1", "avg_tokens", "effective_quality", "qcr"])
        writer.writeheader()
        for r in ablation: writer.writerow({key:r[key] for key in writer.fieldnames})
for n in ["G0_nofeat","G1_feat"]:
    source_file(f"{n}.csv", STUDY.parents[1]/"diag/clean"/f"{n}.csv")
fig,axs=plt.subplots(1,3,figsize=(6.45,2.4),layout="constrained")
for ax,(key,label) in zip(axs,[("acc","准确率"),("macro_f1","宏平均 F1"),("avg_tok","每任务平均通信量 / token")]):
    for i,n in enumerate(["G0_nofeat","G1_feat"]):
        vals=[float(r[key]) for r in rows(DATA/f"{n}.csv") if r["method"]=="EviComRL"]
        ax.bar(i,np.mean(vals),yerr=np.std(vals,ddof=1),capsize=3,color=GRAY if i==0 else BLUE,width=.55)
    ax.set(xticks=[0,1],xticklabels=["无可靠性特征","完整方法"],ylabel=label)
    ax.tick_params(axis="x",labelsize=7.2)
    clean(ax)
save(fig,"reliability")
print(f"Rendered {len(rendered)} figures from bundled EviComRL reports: {', '.join(rendered)}.")
