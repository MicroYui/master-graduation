$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$pptPath = Join-Path $root 'midterm_report_presentation.pptx'

function Convert-Rgb($hex) {
    $h = $hex.TrimStart('#')
    $r = [Convert]::ToInt32($h.Substring(0,2),16)
    $g = [Convert]::ToInt32($h.Substring(2,2),16)
    $b = [Convert]::ToInt32($h.Substring(4,2),16)
    return $r + ($g * 256) + ($b * 65536)
}

function Set-Fill($shape, $hex) {
    $shape.Fill.Visible = -1
    $shape.Fill.Solid()
    $shape.Fill.ForeColor.RGB = Convert-Rgb $hex
}

function Set-Line($shape, $hex, $weight = 0.75) {
    $shape.Line.Visible = -1
    $shape.Line.ForeColor.RGB = Convert-Rgb $hex
    $shape.Line.Weight = $weight
}

function Hide-Line($shape) {
    $shape.Line.Visible = 0
}

function Add-Rect($slide, $x, $y, $w, $h, $fill, $line = $null, $weight = 0.75) {
    $shape = $slide.Shapes.AddShape(1, [single]$x, [single]$y, [single]$w, [single]$h)
    Set-Fill $shape $fill
    if ($line) { Set-Line $shape $line $weight } else { Hide-Line $shape }
    return $shape
}

function Add-Text($slide, $text, $x, $y, $w, $h, $size = 16, $color = '111827', $bold = $false, $align = 1) {
    if ([double]$w -le 0 -or [double]$h -le 0) {
        throw "Invalid text box size for '$text': x=$x y=$y w=$w h=$h"
    }
    $shape = $slide.Shapes.AddTextbox(1, [single]$x, [single]$y, [single]$w, [single]$h)
    $shape.TextFrame.MarginLeft = 0
    $shape.TextFrame.MarginRight = 0
    $shape.TextFrame.MarginTop = 0
    $shape.TextFrame.MarginBottom = 0
    $shape.TextFrame.WordWrap = -1
    $range = $shape.TextFrame.TextRange
    $range.Text = $text
    $range.Font.Name = 'Microsoft YaHei'
    $range.Font.Size = [int][Math]::Round([double]$size)
    $range.Font.Bold = $(if ($bold) { -1 } else { 0 })
    $range.Font.Color.RGB = Convert-Rgb $color
    $range.ParagraphFormat.Alignment = $align
    return $shape
}

function Add-Header($slide) {
    Add-Rect $slide 0 0 960 54 '0878B9' | Out-Null
    Add-Text $slide '存在问题与后续研究' 30 13 430 28 22 'FFFFFF' $true 1 | Out-Null
    Add-Text $slide '硕士学位中期报告' 780 17 150 22 11 'E7F3FA' $false 3 | Out-Null
    Add-Text $slide '硕士学位中期报告' 30 505 140 18 10 '8CA0B3' $false 1 | Out-Null
    Add-Text $slide '11' 895 505 34 18 10 '8CA0B3' $false 3 | Out-Null
}

function Add-Panel($slide, $x, $y, $w, $h, $title, $body, $accent = '1E4976') {
    Add-Rect $slide $x $y $w $h 'F3F5F7' | Out-Null
    Add-Rect $slide $x $y ([Math]::Min($w * 0.38, 150)) 6 $accent | Out-Null
    Add-Text $slide $title ($x + 18) ($y + 24) ($w - 36) 30 18 '1E4976' $true 1 | Out-Null
    if (-not [string]::IsNullOrWhiteSpace($body)) {
        Add-Text $slide $body ($x + 18) ($y + 70) ($w - 36) ($h - 88) 12.5 '222222' $false 1 | Out-Null
    }
}

function Add-Arrow($slide, $x1, $y1, $x2, $y2, $color = '7C8792') {
    $line = $slide.Shapes.AddLine([single]$x1, [single]$y1, [single]$x2, [single]$y2)
    $line.Line.ForeColor.RGB = Convert-Rgb $color
    $line.Line.Weight = 1.5
    $line.Line.EndArrowheadStyle = 3
}

function Add-FlowBox($slide, $x, $y, $w, $h, $title, $body, $fill = 'F3F5F7') {
    Add-Rect $slide $x $y $w $h $fill 'D5DCE3' 0.9 | Out-Null
    Add-Text $slide $title ($x + 10) ($y + 20) ($w - 20) 24 15 '1E4976' $true 2 | Out-Null
    Add-Text $slide $body ($x + 12) ($y + 56) ($w - 24) ($h - 64) 10.5 '222222' $false 2 | Out-Null
}

$app = New-Object -ComObject PowerPoint.Application
$app.Visible = -1
$pres = $app.Presentations.Open($pptPath, $false, $false, $false)
$slide = $pres.Slides.Item(11)

for ($i = $slide.Shapes.Count; $i -ge 1; $i--) {
    $slide.Shapes.Item($i).Delete()
}

Add-Header $slide

Add-Panel $slide 50 92 270 330 '已完成工作的边界' "LEADR 关注物理链路上的功率、能量与队列动态，解决服务数据转发问题。`r`rEviComRL 关注语义消息选择，当前链路条件主要由简化模型给出。`r`r后续需要把链路层的功率开销、能量状态和链路演化引入语义层评估。"

Add-Text $slide '后续连接方式' 362 94 240 26 18 '1E4976' $true 1 | Out-Null
Add-Rect $slide 362 126 495 1.2 'D5DCE3' | Out-Null

Add-FlowBox $slide 360 168 145 118 'LEADR 输出' "链路质量`r功率控制`r节点能量`r存活状态"
Add-FlowBox $slide 562 150 165 154 '约束映射' "送达概率`r传输时延`r丢包风险`r能耗成本" 'EEF3F7'
Add-FlowBox $slide 784 168 145 118 '语义通信评估' "消息选择`r信念更新`r质量--成本`r鲁棒性"
Add-Arrow $slide 505 227 562 227
Add-Arrow $slide 727 227 784 227

Add-Rect $slide 380 328 525 76 'F8FAFC' 'D5DCE3' 0.8 | Out-Null
Add-Text $slide '研究目标' 408 348 96 22 15 '1E4976' $true 1 | Out-Null
Add-Text $slide '在动态链路质量与能量约束下，重新评估选择性语义通信策略的有效性、成本收益和鲁棒性。' 505 346 370 36 12.5 '222222' $false 1 | Out-Null

Add-Panel $slide 380 426 160 50 '链路/能量映射' '' '1E4976'
Add-Text $slide '把物理链路状态转化为语义消息约束' 398 455 124 22 9.5 '222222' $false 2 | Out-Null
Add-Panel $slide 565 426 160 50 '策略重评估' '' '1E4976'
Add-Text $slide '比较 EviComRL 与可部署基线方法' 583 455 124 22 9.5 '222222' $false 2 | Out-Null
Add-Panel $slide 750 426 160 50 '鲁棒性分析' '' '1E4976'
Add-Text $slide '观察质量、成本和资源收紧下的变化' 768 455 124 22 9.5 '222222' $false 2 | Out-Null

$pres.Save()
$pres.Close()
$app.Quit()



