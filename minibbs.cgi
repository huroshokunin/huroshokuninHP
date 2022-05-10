#!/usr/local/bin/perl

;# 簡易ＢＢＳ version 10.32
;#
;# This is Freeware.
;# (c)1996-2008 by CGI-RESCUE
;# Scripts Found at: http://www.rescue.ne.jp/

# [基本仕様]
#
# ※ 旧バージョンとのデータ互換はありません.
# ※ METHOD=POST専用です.
# ※ S-JIS設置専用です.
# ※ 西暦2000年対応.

# [基本構成] ( )内は設定する必要があるパーミッション値
#
#   /public_html/（ホームページディレクトリ）
#        |
#        |-- /cgi-bin/（任意のディレクトリ）
#                |
#                |-- jcode.pl
#                |-- minibbs.cgi (755)
#                |
#                |-- /data/ (777)
#                       |
#                       |-- data.cgi

# [履歴]
#
# v1.0   02/MAY/96 初版
# v8.90  11/AUG/98 v8.8にロック機能を付加
# v9.00  12/AUG/98 タグ処理を制限してセキュリティアップ
# v9.01  24/AUG/98 未入力処理(クッキー消去)時にリストされな不具合を修正
# v9.02  03/SEP/98 改行の扱いを３種類に変更
# v9.03  18/SEP/98 Ｅメール自動リンクの廃止
# v9.04  19/OCT/98 タブコードの取り扱い修正
# v9.05  26/OCT/98 記録データ制限の解除処理
# v9.06  22/NOV/98 エラー処理を改善
# v10.00 24/NOV/98 検索機能の追加および構造変更
# v10.01 02/DEC/98 クッキー機能の修正ほか
# v10.02 08/DEC/98 Ｄ系トラブルの修正
# v10.10 08/DEC/98 ２重(連続)投稿防止処理
# v10.11 08/DEC/98 削除キー削除が出来なくなったバグの修正
# v10.12 15/DEC/98 パスワード強化
# v10.13 17/DEC/98 全角文字マッチの不具合の訂正
# v10.14 21/DEC/98 ファイルを閉じていない個所の修正,メールアドレス形式チェック方法の変更
# v10.15 14/FEB/99 記事最後案内の修正
# v10.20 19/FEB/99 新着記事のマーキング
# v10.21 20/FEB/99 通算日数計算のバグ修正
# v10.30 08/JUL/99 ロック処理のバグ修正,ロック処理方法の変更,暗号処理のベリファイ機能付加
# v10.31 04/SEP/99 暗号処理部分の修正
# v10.32 13/DEC/08 クロスサイト・スクリプティング脆弱性を修正(※1) , 削除キー保存機能の無効化 , メールアドレスのエンティティー化

# [データ形式]
#
# ※ 各記事は１件１行とし、各項目はタブ区切りとする.
# ※ 各項目の並びは次の通り.
#
# 識別番号 暗号パスワード 投稿者 Ｅメール ホスト名 投稿時刻 題名 記録タイプ リンクの有無 内容 ２重投稿チェック用文字列

#----------------#
#    初期設定    #
#----------------#

#--- 必ずあなたの環境に合わせて書き替える項目 --------------------------------------------#

#◆掲示板の名前
#　''内に記述しますが、'を入れたい場合は '' を "" に替えてください.
#　ただしその場合、文字によって化けが生じることがあります.
#　詳しくは当サイトのＦＡＱを参照してください.
$title = '簡易ＢＢＳ';

#◆このスクリプトをＵＲＬで設定
$reload = 'http://設置したＵＲＬ/minibbs.cgi';

#◆画面の「終了」リンク先をＵＲＬで設定
$modoru = 'http://ホームページなどのＵＲＬ/';


#--- 必要に応じて設定する項目 ------------------------------------------------------------#

#◆画面の色や背景の設定 (HTML書式)
$body = '<body bgcolor=#000000 text=#ffffff link=#ff8888 vlink=#ffaaaa>';

#◆見出の色
$midashi_color = '#ffeedd';

#◆記事題名の色
$subject_color = '#ff88aa';

#◆記事ヘッダ(名前や投稿日など)の色
$head_color = '#ffeedd';

#◆記事内容の色
$body_color = '#ffffff';

#◆記事(通常時)内容の文字サイズ(CSS設定)
$span_size = 'small';

#◆記事(図表モード時)内容の文字サイズ(CSS設定)
$pre_size = 'small';

#◆ホスト名の表示の可否 1:する 0:しない
$view_host = 1;

#◆２重(連続)投稿チェックの対象にする行数
$njmax = 10;

#◆画面内に記述する文字列等 (HTML書式)
#　''内に記述しますが、'を入れたい場合は '' を "" に替えてください.
#　ただしその場合、文字によって化けが生じることがあります.
#　詳しくは当サイトのＦＡＱを参照してください.
#　必要ない場合は '' 内に何も書きません.

#◆(見出)タイトルの下位置に表示する文字列
$msg_top = '

';

#◆(見出)投稿フォームの下位置に表示する文字列
$msg_mid = '

';

#◆(見出)最下部に表示する文字列
$msg_btm = '

※ すべてのボタンは１回だけ押してしばらくお待ちください.<br>
※ [削除]ボックスをチェックして、投稿時に設定した削除キーを入力してボタンを押せば削除できます.<br>
※ 検索文字列はスペースで区切ることで複数指定できます.<br>
※ 複数指定時にはそれぞれの文字列に対して、AND(かつ) OR(または)を適用します.<br>
※ 削除キー欄にマスターキー(管理者のみ)を入力すると任意の記事の削除が可能です.
';

#◆$reloadで設定した設置ＵＲＬ以外のフォームからの投稿を禁止する処置 する:1 しない:0
#　悪戯の防止用ですが、利用サーバやブラウザによっては正規投稿もできなくなる場合もあります.
$ref_axs = 0;

#◆１画面に表示する件数
$def = 10;

#◆新着マーク(New画像)を表示する日数
$update = 7;

#◆書き込み件数の最大登録数の設定です。この件数を超えると、古いものから削除されていきます.
#　ページ処理機能が付きましたので、この件数を大きくしても一度に表示される記事数は限定されます.
#　サーバの負担を考慮し、できるだけ500以下程度に設定しましょう。
$max = '300';

#◆日本語コード変換ライブラリ
#　minibbs.cgiと同じ場所に設置する場合はこのままでよい.
require './jcode.pl';

#◆内容が書き込まれる記録ファイルの名前（パスの設定ではない！）
$file = 'data.cgi';

#◆データディレクトリのパスの設定（処理の都合上 / で閉じない）
$tmp_dir = './data';

#◆海外サーバ等で時差が生じる場合は修正
#　＋９時間する場合　= localtime(time + 9*60*60);
#　－９時間する場合　= localtime(time - 9*60*60);
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);

#◆クッキーの消化設定
#　最終書き込みから   30日後 30*24*60*60
#　　　　　　　　　　　1日後 24*60*60
#　　　　　　　　　 10時間後 10*60*60
($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg) = gmtime(time + 30*24*60*60);

#------------------

$cmd = $ENV{'QUERY_STRING'};
if ($cmd eq 'copyright') { &copyright; exit; }
elsif ($cmd eq 'new') { &new; exit; }

@wday_array = ('日','月','火','水','木','金','土');
$date_now = sprintf("%04d年%01d月%01d日(%s)%02d時%02d分",$year +1900,$mon +1,$mday,$wday_array[$wday],$hour,$min);
$date_num = sprintf("%04d%02d%02d%02d%02d%02d",$year +1900,$mon +1,$mday,$hour,$min,$sec);

$days[4] = $days[6] = $days[9] = $days[11] = 30;
$days[1] = $days[3] = $days[5] = $days[7] = $days[8] = $days[10] = $days[12] = 31;

$days_now = &Days($year +1900,$mon +1,$mday);

$ps = $$;
if ($ps eq '') { $ps = $date_num; }
$tmp_file = "$ps\.tmp";

read(STDIN,$buffer,$ENV{'CONTENT_LENGTH'});

@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {

	($name,$value) = split(/=/,$pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
	&jcode'convert(*value,'sjis');

	$value =~ s/\&/&amp;/g;
	$value =~ s/\"/&quot;/g;
	$value =~ s/</&lt;/g;
	$value =~ s/>/&gt;/g;
	$value =~ s/\t//g;

	$value =~ s/\r\n/\r/g;
	$value =~ s/\n/\r/g;

	if ($name eq 'target') { push(@RM,$value); }
	else { $FORM{$name} = $value; }
}

$cookies = $ENV{'HTTP_COOKIE'};

@pairs = split(/;/,$cookies);
foreach $pair (@pairs) {

	($name,$value) = split(/=/,$pair,2);
	$name =~ s/ //g;

	$value =~ s/\"/&quot;/g; # ※1
	$value =~ s/</&lt;/g;
	$value =~ s/>/&gt;/g;

	$DUMMY{$name} = $value;
}

@pairs = split(/,/,$DUMMY{$reload});
foreach $pair (@pairs) {

	($name,$value) = split(/:/,$pair,2);
	$COOKIE{$name} = $value;
}

if (-z "$tmp_dir\/$file") { $first = 1; }

if ($FORM{'action'} eq 'setpwd') { &setpwd; &search; &html; exit; }
elsif ($first) { &password; exit; }
elsif ($FORM{'admin'} eq 'change') { &password; exit; }
elsif (@RM && $FORM{'action'} eq 'remove') { &remove; }
elsif ($FORM{'action'} eq 'regist') { &regist; }

&search;
&html;
exit;

#------------------

sub search {

	if ($FORM{'search'} ne '') {

		$i = $FORM{'search'};
		$i =~ s/　/ /g;
		$keys = $i;
		&jcode'convert(*i,'euc');
		$i =~ s/(\W)/\\$1/g;
		$target = $i;
		@keys = split(/\\\s+/,$target);
	}

	if (!open(READ,"$tmp_dir\/$file")) { &error('エラー','データが読み出せません.'); }
	$master = <READ>;
	unless ($master =~ /^MiniBBSv10:(.+)$/) { &error('エラー','データの形式が違います.'); }

	if ($FORM{'page'} eq '') { $page = 1; } else { $page = $FORM{'page'}; }

	$page_control = $hit = $allhits = $all = 0;
	if ($FORM{'action'} ne 'remove') { $start = (times)[0]; }

	while (<READ>) {

		$string = $string_s = $_;

		$page_control++;
		if ($page > $page_control) { next; }

		if ($FORM{'search'} ne '') {

			if ($FORM{'page'} eq '') { $all++; }
			&jcode'convert(*string,'euc');

			if ($FORM{'mode'} eq 'or') {

				$match = 1;
				foreach $term (@keys) {

					if ($string =~ /^([\x00-\x7F]|[\x8E\xA1-\xFE][\xA1-\xFE]|\x8F[\xA1-\xFE]{2})*$term/i) { $match = 0; }
				}
			}
			else {

				$match = 0;
				foreach $term (@keys) {

					if (!($string =~ /^([\x00-\x7F]|[\x8E\xA1-\xFE][\xA1-\xFE]|\x8F[\xA1-\xFE]{2})*$term/i)) { $match = 1; }
				}
			}

			if ($match) { next; }

			if ($FORM{'page'} ne '') {

				$allhits = $FORM{'allhits'};
				if ($hit == $def) { $next_num = $page_control; last; }
				else { push(@PICKUP,$string_s); $hit++; }
			}
			else {
				if ($end != 1 && $hit == $def) { $end = 1; $next_num = $page_control; $allhits++; }
				elsif ($hit >= $def) { $allhits++; }
				else { push(@PICKUP,$string_s); $hit++; $allhits++; }
			}
		}
		else {
			$hit++;
			if ($hit > $def) { $next_num = $page_control; last; }
			else { push(@PICKUP,$string_s); }
		}
	}

	if ($FORM{'action'} ne 'remove') { $end = (times)[0]; }
	$cpu = sprintf("%.3f",$end - $start);
	close(READ);
}

sub html {

	if (!@PICKUP && $page != 0) { $FORM{'page'} = $page - 1; &search; }

	$nj = '';
	@char = ('a'..'z','A'..'Z','0'..'9');
	srand(time|$$);
	foreach (0..9) {
		{
			local(@temp);
			push(@temp,splice(@char,rand(@char),1)) while @char;
			@char = @temp;
		}
		$nj = $char[($_)] . $nj;
	}

	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title>\n";
	print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=Shift_JIS\">\n";
	print "<style type=\"text/css\">\n";
	print "<!--\n";
	print "pre {font-size:$pre_size; color:$body_color;}\n";
	print "span {font-size:$span_size; color:$body_color;}\n";
	print "-->\n";
	print "</style>\n";
	print "</head>\n";

	print "$body\n";
	print "<h1>$title</h1>\n";

	print "$msg_top<p>\n";

	print "<form method=POST action=\"$reload\">\n";
	print "<input type=hidden name=\"action\" value=\"regist\">\n";
	print "<input type=hidden name=\"nj\" value=\"$nj\">\n";

	print "<table>\n";
	print "<tr><td>投稿者</td><td><input type=text name=\"name\" size=21 value=\"$COOKIE{'name'}\" maxlength=20></td></tr>\n";
	print "<tr><td>Ｅメール</td><td><input type=text name=\"email\" size=40 value=\"$COOKIE{'email'}\"></td></tr>\n";
	print "<tr><td>題名</td><td><input type=text name=\"subject\" size=51 maxlength=50></td></tr>\n";
	print "<tr><td colspan=2>内容 <font size=-1> ";
	print "<input type=radio name=\"how\" value=\"2\" checked>改行有効 ";
	print "<input type=radio name=\"how\" value=\"0\">改行無効 ";
	print "<input type=radio name=\"how\" value=\"1\">図/表\モード ";
	print "<input type=checkbox name=\"link\" value=\"1\" checked>URLをリンクする</font></td></tr>\n";
	print "<tr><td colspan=2><textarea name=\"value\" rows=5 cols=70 wrap=off></textarea></td></tr>\n";

	print "<tr><td>削除キー</td><td><input type=password name=\"pwd\" size=10 value=\"\"> ";
	print "<input type=checkbox name=\"cookie\" value=\"on\" checked><font size=-1>投稿者とメールを保存</font></td></tr></table>\n";
	print "<input type=submit value=\"     Ｏ  Ｋ     \"><input type=reset value=\"キャンセル\"></form><p>";
	print "<font size=-1 color=$midashi_color>$msg_mid</font><p>\n";

	print "<strong><font size=+1>[<a href=\"$reload\">更新</a>] [<a href=\"$modoru\" target=\"_top\">終了</a>]</font></strong>\n";
	print "<p><hr size=3 noshade><font size=-1>\n";

	if ($FORM{'mode'} eq 'or') { $OR = 'checked'; $MODE = '(または)'; }
	elsif ($FORM{'mode'} eq 'and' || $FORM{'mode'} eq '') { $AND = 'checked'; $MODE = '(かつ)'; }
	unless ($keys =~ / /) { $MODE = ''; }

	if ($next_num ne '') { $page_end = $page + $hit - 2; }
	else { $page_end = $page + $hit - 1; }

	if ($page_end <= 0) {

		if ($FORM{'search'} ne '') { print "<strong>指定の文字列を含む記事はありません.</strong> (検索時間 $cpu CPU秒) "; }
		else { print "<strong>記事はありません.</strong> "; }
	}
	elsif ($page <= $page_end && $FORM{'search'} eq '' && !$next_num) {

		print "<strong>新着順</strong> $page → 最後 ";
		print "<strong>最大記録保持数</strong> $max ";
	}
	else {

		if ($FORM{'search'} ne '') {

			if ($all == 0) { $all = $FORM{'all'}; }

			print "<strong>《検索モード》 文字列</strong> &quot;$keys&quot; $MODE ";

			if ($FORM{'action'} ne 'remove') {

				print "<strong>抽出数</strong> $allhits ";
				print "<strong>抽出位置</strong> $page<sub>/総数$all</sub>～ ";
				print "<strong>検索時間</strong> $cpu CPU秒 ";
			}
			else { print "<!-- 実行時間 $cpu CPU秒 -->"; }
		}
		else {

			print "<strong>新着順</strong> $page → $page_end ";
			print "<strong>最大記録保持数</strong> $max ";
			print "<!-- 実行時間 $cpu CPU秒 -->";
		}
	}

	print "(<img src=\"$reload\?new\" alt=\"New!\" width=22 height=10>は$update日以内の記事)</font>\n";

	if ($page_end > 0) {

		print "<form method=POST action=\"$reload\">\n";
		print "<input type=hidden name=\"action\" value=\"remove\">\n";
		print "<input type=hidden name=\"page\" value=\"$page\">\n";
		print "<input type=hidden name=\"all\" value=\"$all\">\n";
		print "<input type=hidden name=\"allhits\" value=\"$allhits\">\n";
		print "<input type=hidden name=\"search\" value=\"$keys\">\n";
		print "<input type=hidden name=\"mode\" value=\"$FORM{'mode'}\">\n";

		foreach (@PICKUP) {

			($number,$pwd,$name,$email,$host,$date,$subject,$how,$link,$value,$nj) = split(/\t/);

			if ($number =~ /^(\d\d\d\d)(\d\d)(\d\d)/) {

				$y = $1;
				$m = sprintf("%d",$2);
				$d = sprintf("%d",$3);
			}

			$days = &Days($y,$m,$d);
			$upd = $days_now - $days;
			if ($upd <= $update) { $new = "<img src=\"$reload\?new\" alt=\"New!\"> "; } else { $new = ""; }

			$value =~ s/&quot;/\"/g;
			$value =~ s/&amp;/\&/g;
			if ($link == 1) { $value =~ s/(https?|ftp|gopher|telnet|whois|news)\:([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<a href=\"$1\:$2\" target=\"_blank\">$1\:$2<\/a>/ig; }

			if ($view_host) { $host = "[$host]"; }
			else { $host = ""; }

			print "<font size=+1 color=$subject_color><hr size=1>$new$subject</font><br>\n";

			print "<font size=-1 color=$head_color>";
			print "　<strong>投稿日</strong> $date ";

			if ($email ne '') {

				$email =~ s/\@/&#64;/g;
				print "<strong>投稿者</strong> <a href=\"mailto:$email\">$name</a> $host";
			}
			else { print "<strong>投稿者</strong> $name $host"; }

			print " <input type=checkbox name=\"target\" value=\"$number\">削除<p>\n";
			print "</font>\n";

			print "<blockquote>\n";

			if ($how == 1) { print "<pre>$value</pre><p>\n"; }
			elsif ($how == 2) { $value =~ s/\r/<br>\r/g; print "<span>$value</span><p>\n"; }
			else { print "<span>$value</span><p>\n"; }

			print "</blockquote>\n";
		}
	}

	print "<hr size=3 noshade>\n";
	print "<p><table border=3 cellpadding=1 cellspacing=2><tr>\n";

	if ($page_end > 0) {

		print "<td align=center>削除キー <input type=password name=\"pwd\" size=10 value=\"$COOKIE{'pwd'}\"> ";
		print "<input type=submit value=\"削除\"></td></form>\n";
	}

	if ($next_num ne '') {

		print "<form method=POST action=\"$reload\">\n";
		print "<input type=hidden name=\"page\" value=\"$next_num\">\n";
		print "<input type=hidden name=\"all\" value=\"$all\">\n";
		print "<input type=hidden name=\"allhits\" value=\"$allhits\">\n";
		print "<input type=hidden name=\"search\" value=\"$keys\">\n";
		print "<input type=hidden name=\"mode\" value=\"$FORM{'mode'}\">\n";
		print "<td align=center><input type=submit value=\"次のページ\"></td></tr></form><tr>\n";
	}

	print "<form method=POST action=\"$reload\">\n";
	print "<td>文字列 <input type=text name=\"search\" value=\"$keys\" size=15>\n";
	print "<input type=radio name=\"mode\" value=\"and\" $AND>AND <input type=radio name=\"mode\" value=\"or\" $OR>OR\n";
	print "<input type=submit value=\"検索\"></td></form>\n";

	print "<td align=center><strong><font size=+1>[<a href=\"$reload\">更新</a>] [<a href=\"$modoru\" target=\"_top\">終了</a>]</font></strong></td>\n";
	print "</tr></table><p>\n";

	print "<font size=-1 color=$midashi_color>$msg_btm</font><p>\n";

	print "<br><br><br>\n";
	print "<form method=POST action=\"$reload\">\n";
	print "<input type=hidden name=\"admin\" value=\"change\">";
	print "<input type=submit value=\"管理キー変更\"></form>\n";

	# このスクリプトの著作権表示（かならず表示してください）
	print "<h5 align=right><a href=\"http://www.rescue.ne.jp/\" target=\"_top\"><img src=\"$reload\?copyright\" border=0 alt=\"MiniBBS v10.32\"></a></h5>\n";

	print "</body></html>\n";
}

sub regist {

	if ($ref_axs) {

		$ref = $ENV{'HTTP_REFERER'};
		$ref =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
		if (!($ref =~ /$reload/)) { &error('利用不可',"次のページ以外からの投稿は受け付けられません.<br>→ $reload"); }
	}

	if (!open(READ,"$tmp_dir\/$file")) { &error('エラー','データが読み出せません.'); }
	$master = <READ>;
	unless ($master =~ /^MiniBBSv10:(.+)$/) { &error('エラー','データの形式が違います.'); }

	if ($FORM{'name'} eq '') { &error('入力ミス','投稿者を記入してください.'); }
	if ($FORM{'name'} =~ /\;/) { &error('入力ミス','投稿者にセミコロンは使えません.'); }
	if ($FORM{'name'} =~ /\,/) { &error('入力ミス','投稿者にカンマは使えません.'); }

	if ($FORM{'email'} ne '' && !($FORM{'email'} =~ /\b[-\w.]+@[-\w.]+\.[-\w]+\b/)) { &error('入力ミス','Ｅメールの形式が間違っています.'); }
	if ($FORM{'email'} =~ /\;/) { &error('入力ミス','Ｅメールにセミコロンは使えません.'); }
	if ($FORM{'email'} =~ /\,/) { &error('入力ミス','Ｅメールにカンマは使えません.'); }

	if ($FORM{'subject'} eq '') { &error('入力ミス','題名を記入してください.'); }
	if ($FORM{'value'} eq '') { &error('入力ミス','内容を記入してください.'); }

	if ($FORM{'pwd'} eq '' || length($FORM{'pwd'}) < 6) { &error('入力ミス','削除キー欄に6文字以上の半角文字でパスワードを指定してください.<br>これは記事を削除する時に利用するものです.'); }
	&encode2($FORM{'pwd'});

	$j = 0;
	while (<READ>) {

		$j++;
		if ($j > $njmax) { last; }

		($i,$i,$i,$i,$i,$i,$i,$i,$i,$i,$nj) = split(/\t/);
		if ($nj =~ /$FORM{'nj'}/) { &error('二重(連続)投稿の禁止',"ＯＫボタンを２回以上押した可能\性がありますので、投稿されているかどうかご<a href=\"$reload\">確認</a>ください.<br>再投稿は<a href=\"$reload\">更新</a>してからご利用ください."); }
	}
	close(READ);

	$y0="Sunday"; $y1="Monday"; $y2="Tuesday"; $y3="Wednesday"; $y4="Thursday"; $y5="Friday"; $y6="Saturday";
	@youbi = ($y0,$y1,$y2,$y3,$y4,$y5,$y6);

	$m0="Jan"; $m1="Feb"; $m2="Mar"; $m3="Apr"; $m4="May"; $m5="Jun";
	$m6="Jul"; $m7="Aug"; $m8="Sep"; $m9="Oct"; $m10="Nov"; $m11="Dec";
	@monthg = ($m0,$m1,$m2,$m3,$m4,$m5,$m6,$m7,$m8,$m9,$m10,$m11);

	$date_gmt = sprintf("%s\, %02d\-%s\-%04d %02d:%02d:%02d GMT",$youbi[$wdayg],$mdayg,$monthg[$mong],$yearg +1900,$hourg,$ming,$secg);

	if ($FORM{'cookie'} eq 'on') {

		$cook="name\:$FORM{'name'}\,email\:$FORM{'email'}";
		print "Set-Cookie: $reload=$cook; expires=$date_gmt\n";

		$COOKIE{'name'} = $FORM{'name'};
		$COOKIE{'email'} = $FORM{'email'};
	}
	else {

		print "Set-Cookie: $reload=\n";
		$COOKIE{'name'} = $COOKIE{'email'} = '';
	}

	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};
	if ($host eq '') { $host = $addr; }
	if ($host eq $addr) { $host = gethostbyaddr(pack('C4',split(/\./,$host)),2) || $addr; }

	&lock1;

	if (!open(READ,"$tmp_dir\/$file")) { &error('エラー','データが読み出せません.'); }
	$master = <READ>;

	if (!open(WRITE,"> $tmp_dir\/$tmp_file")) { &error('エラー','テンポラリーファイルが作成できません.'); }
	print WRITE $master;
	print WRITE "$date_num\t$pwd\t$FORM{'name'}\t$FORM{'email'}\t$host\t$date_now\t$FORM{'subject'}\t$FORM{'how'}\t$FORM{'link'}\t$FORM{'value'}\t$FORM{'nj'}\n";

	$max_control = 0;
	while (<READ>) {

		$max_control++;
		print WRITE;
		if ($max_control == $max - 1) { last; }
	}

	close(WRITE);
	close(READ);

	&lock2;
}

sub error {

	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=Shift_JIS\">\n";
	print "$body\n";
	print "<h1>$_[0]</h1>\n";
	print "<h3>$_[1]</h3>\n";
	print "ブラウザの[戻る]ボタンを押して前の画面に移動してください.<p>\n";
	print "</body></html>\n";
	exit;
}

sub remove {

	&lock1;

	if (!open(READ,"$tmp_dir\/$file")) { &error('エラー','データが読み出せません.'); }
	$master = <READ>;

	chop($master);
	($vers,$crypted_pwd) = split(/:/,$master);
	if ($crypted_pwd =~ /^\$1\$/) { $salt = 3; } else { $salt = 0; }
	if (crypt($FORM{'pwd'},substr($crypted_pwd,$salt,2)) eq $crypted_pwd) { $admin = 1; } else { $admin = 0; }

	$target = join('|',@RM);

	if (!open(WRITE,"> $tmp_dir\/$tmp_file")) { &error('設定ミス','テンポラリーファイルが作成できません.'); }
	print WRITE "$master\n";

	$start = (times)[0];

	while (<READ>) {

		($number,$pwd,$name,$email,$host,$date,$subject,$how,$link,$value,$nj) = split(/\t/);

		if ($number =~ /$target/) {

			if ($admin || crypt($FORM{'pwd'},substr($pwd,$salt,2)) eq $pwd) { next; }
		}

		print WRITE;
	}

	$end = (times)[0];
	close(WRITE);
	close(READ);

	&lock2;
}

sub password {

	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=Shift_JIS\">\n";
	print "$body\n";
	print "<h1>マスターキーの設定/変更</h1>\n";

	if ($first && $message eq '') { print "掲示板新規開設にあたり、管理キーを登録してください。<p>\n"; }
	else { print "$message<p>\n"; }

	print "<form method=POST action=\"$reload\">\n";
	print "<input type=hidden name=\"action\" value=\"setpwd\">\n";
	if (!$first) { print "現在の管理キー <input type=password name=\"password_old\" size=10><br>\n"; }
	print "新管理キー <input type=password name=\"pwd\" size=10><br>\n";
	print "新管理キー <input type=password name=\"pwd2\" size=10> (確認のためもう一度)<p>\n";
	print "<input type=submit value=\"     Ｏ  Ｋ     \"></form><p>\n";
	print "</body></html>\n";
}

sub setpwd {

	&lock1;

	if (!open(READ,"$tmp_dir\/$file")) { &error('エラー','データが読み出せません.'); }
	$master = <READ>;

	chop($master);
	($vers,$crypted_pwd) = split(/:/,$master);
	if ($crypted_pwd =~ /^\$1\$/) { $salt = 3; } else { $salt = 0; }

	if ($vers eq 'MiniBBSv10') {

		if (crypt($FORM{'password_old'},substr($crypted_pwd,$salt,2)) ne $crypted_pwd) { $message = '現在の管理キーが認証されません.'; &password; exit; }
	}
	if ($FORM{'pwd'} =~ /\W/ || $FORM{'pwd'} eq '') { $message = '新管理キーに英数字以外の文字が含まれているか空欄です.'; &password; exit; }
	if ($FORM{'pwd'} ne $FORM{'pwd2'}) { $message = '確認のために入力された新管理キーが一致しません.'; &password; exit; }
	if (length($FORM{'pwd'}) < 8) { $message = '8文字以上の半角文字でパスワードを指定してください.'; &password; exit; }

	&encode2($FORM{'pwd'});

	if (!open(WRITE,"> $tmp_dir\/$tmp_file")) { &error('エラー','テンポラリーファイルが作成できません.'); }
	print WRITE "MiniBBSv10\:$pwd\n";
	while (<READ>) { print WRITE; }

	close(WRITE);
	close(READ);

	&lock2;
}

sub encode2 {

	$plain = $_[0];
	$now = time;
	($p1, $p2) = unpack("C2", $now);
	$wk = $now / (60*60*24*7) + $p1 + $p2 - 8;
	@saltset = ('a'..'z','A'..'Z','0'..'9','.','/');
	$nsalt = $saltset[$wk % 64] . $saltset[$now % 64];
	if (!eval '$pwd = crypt($plain,$nsalt);') { &error('エラー','暗号処理ができません.'); }
	if ($pwd =~ /^\$1\$/) { $salt = 3; } else { $salt = 0; }
	if (crypt($plain,substr($pwd,$salt,2)) ne $pwd) { &error("暗号処理エラー","パスワード(削除キー)の暗号化に失敗しました. 戻って再度実行してください."); }
}

sub lock1 {

	$od_check = (eval { opendir(DIR,"$tmp_dir"); }, $@ eq "");
	if (!$od_check) { &error("システムエラー1",""); }

	@list = readdir(DIR);
	closedir(DIR);

	if (!@list) { &error("システムエラー2",''); }
	@lists = grep(/\.tmp/,@list);

	local($retry) = 3;
	while (@lists) {

		if (--$retry <= 0) {

			foreach (@lists) { if (-e "$tmp_dir\/$_") { unlink("$tmp_dir\/$_"); }}
			&error("Busy(1)",'ただ今混雑しております.<br>時間をおいて再度実行してください.');
		}

		sleep(1);

		opendir(DIR,"$tmp_dir");
		@list = readdir(DIR);
		closedir(DIR);
		@lists = grep(/\.tmp/,@list);
	}
}

sub lock2 {

	opendir(DIR,"$tmp_dir");
	@list = readdir(DIR);
	closedir(DIR);

	@lists = grep(/\.tmp/,@list);
	@lists = grep(!/$tmp_file/,@lists);

	if (@lists) {

		if (-e "$tmp_dir\/$tmp_file") { unlink("$tmp_dir\/$tmp_file"); }
		&error("Busy(2)",'書き込みに失敗しました.');
	}

	if (!rename("$tmp_dir\/$tmp_file","$tmp_dir\/$file")) { &error("Busy(3)",'書き込みに失敗しました.<br>再度実行してください.'); } ;
	chmod 0666,"$tmp_dir\/$file";
}

sub Days {

	local ($year,$month,$day) = @_;
	local ($base,$i,$y);

	$days[2] = 28;
	unless ($year % 4) { $days[2] = 29; }
	unless ($year % 100) { $days[2] = 28; }
	unless ($year % 400) { $days[2] = 29; }

	$y = $year - 1;
	$base = ($y * 365) + ($y / 4) - ($y / 100) + ($y / 400) - 1;

	$i = $month;
	while ( --$i ) { $base += $days[$i]; }

	return int($base + $day);
}

sub new {

	@array = (
	"47","49","46","38","39","61","16","00","0a","00","b3","02","00","00","00","00","ff","d6","00","ff",
	"ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff",
	"ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff",
	"ff","21","f9","04","01","00","00","02","00","2c","00","00","00","00","16","00","0a","00","40","04",
	"37","50","c8","29","02","ad","77","06","60","2b","0f","60","b8","71","00","e7","99","db","88","7e",
	"21","ab","81","65","1c","be","70","4d","8a","69","6e","66","38","98","49","29","e0","4d","b4","f3",
	"d8","8e","3e","c1","67","59","3b","a9","4a","47","54","12","c3","eb","09","22","00","3b");

	print "Content-type: image/gif\n\n";
	foreach (@array) { $data = pack('C*',hex($_)); print $data; }
	exit;
}

sub copyright {

	@array = (
	"47","49","46","38","39","61","27","00","1a","00","b3","00","00","00","00","00","ff","ff","ff","00",
	"00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
	"00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","92","92","92","00","00",
	"00","21","f9","04","01","00","00","00","00","2c","00","00","00","00","27","00","1a","00","40","04",
	"b6","10","c8","49","ab","bd","d8","86","e0","b6","fb","1b","d7","01","5e","08","92","60","19","5c",
	"62","e7","b9","9f","2b","be","e1","86","d5","38","89","87","d2","6e","67","93","d6","88","33","eb",
	"f1","76","41","5e","c5","c7","6c","fa","58","29","14","cc","25","f5","9d","80","ad","df","2b","75",
	"bd","75","7b","d3","52","2a","2b","8c","6d","57","46","22","6d","cd","e6","ca","be","94","b2","59",
	"7e","da","c2","e3","f2","5a","6c","2e","e5","b3","da","6f","81","6c","44","40","69","3f","86","48",
	"19","35","1a","59","3a","73","34","58","70","62","81","63","6a","2a","32","25","1a","61","61","8e",
	"6f","26","82","4b","94","67","55","55","2a","45","14","7b","97","a9","a9","00","66","7b","ac","7f",
	"4e","4c","88","87","7f","63","b7","82","a6","54","8a","b8","9f","be","67","b5","50","bd","64","45",
	"9f","77","71","75","33","c5","ca","23","28","c1","41","ad","af","c6","a9","d3","51","85","d7","d8",
	"19","11","00","00","3b");

	print "Content-type: image/gif\n\n";
	foreach (@array) { $data = pack('C*',hex($_)); print $data; }
	exit;
}
