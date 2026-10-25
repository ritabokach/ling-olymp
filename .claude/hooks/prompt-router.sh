#!/usr/bin/env bash
# UserPromptSubmit hook — the user never has to type skill names. Every prompt gets:
#   1) the always-on writing rules (caveman + anti-slop in chat),
#   2) the intent → skill map, plus a "likely skill" hint when the words clearly match.
# Context only, never blocks. Fail-open.
set -euo pipefail
trap 'exit 0' ERR
command -v jq >/dev/null 2>&1 || exit 0

P="$(jq -r '.prompt // empty')"
[ -n "$P" ] || exit 0
case "$P" in /*) exit 0 ;; esac            # explicit slash command: no routing needed

# perl with UTF-8: case-insensitive Cyrillic matching (grep/tr in the C locale cannot).
hint="$(P="$P" perl -CSDA -Mutf8 -e '
  my $p = $ENV{P}; utf8::decode($p) unless utf8::is_utf8($p);
  my @r = (
    [ qr/работаем ночью|поработай ночью|^\W*ночь(?![а-яё])|ночн\w* режим|режим ночь|оставл\w*(?: \w+)? на ночь|пока (я )?сплю|^\W*night\b|night mode/i, "/night" ],
    [ qr/стоп ноч|останови ноч|проснул|night-stop/i,                                   "/night-stop" ],
    [ qr/глубок\w* (ресеч|ресерч|research|исследован|поиск)|deep research|tavily|тавил|тевил|тэвил/i, "/research DEEP level (Tavily)" ],
    [ qr/ресеч|ресерч|research|исследу|найди (в интернете|информ\w*|инфу|всё|все)|поищи|погугли/i, "/research BASIC level (WebSearch, no Tavily)" ],
    [ qr/\.(mp3|mp4|m4a|wav|webm|ogg|flac|mov)\b|расшифр|транскриб|запись встречи/i, "/transcribe" ],
    [ qr/агент(а)? под|новый агент|new[- ]agent|исполнител(я|ь) под/i,                "/new-agent" ],
    [ qr/дефраг|почисти (memory|мемори|память)|актуализируй (memory|мемори)|defrag/i, "/memory-bank-defrag" ],
    [ qr/постав(ь|и) харнесс|установи харнесс|install (the )?harness/i,               "/setup" ],
    [ qr/не работает|сломал|ошибк|падает|упал|traceback|exception|stack ?trace|\berror\b|(?<![а-яё])баг/i, "/debug" ],
    [ qr/мутаци|mutation|проверь тесты|тесты что-то проверяют|насколько хорош\w* тест/i,  "/mutation" ],
    [ qr/ревью|отревью|\breview\b|проверь (код|изменения|pr|пр)/i,                    "/review" ],
    [ qr/напиши (текст|пост|письм|сообщени|описани|readme|доку)|перепиши текст|тексты? для бота/i, "/anti-ai-slop-writing" ],
  );
  for my $x (@r) { if ($p =~ $x->[0]) { print $x->[1]; last } }
' 2>/dev/null || true)"

CTX="HARNESS ROUTER: write per .claude/skills/anti-ai-slop-writing (chat: caveman + bans). Skills fire from intent (AGENTS.md → «Skills fire by themselves»). Subagent prompts start with the caveman lines; reports short, details to files. Questions only at checkpoints, options with плюсы/минусы. End reply with Memory Bank Steward check."
[ -n "$hint" ] && CTX="$CTX
Likely skill for this prompt: $hint — invoke it (Skill tool) unless the request clearly means something else."

jq -nc --arg c "$CTX" '{hookSpecificOutput:{hookEventName:"UserPromptSubmit", additionalContext:$c}}'
