# Sending Gmail using CLI on macOS

- [Sending Gmail using CLI on macOS](#sending-gmail-using-cli-on-macos)
  - [Install NeoMutt](#install-neomutt)
  - [Configuration](#configuration)
  - [CLI to send email](#cli-to-send-email)

The goal is to **send** Gmail using CLI (so we can schedule it with crontab for automation), *without downloading* any mails to a local mailbox. Technically speaking, we need SMTP only and not IMAP/POP3.

## Install NeoMutt

```
brew install neomutt
```

## Configuration

NeoMutt keeps the compatibility with muttrc, so we can reuse the path

> The config is not minimal, but it works

~/.config/mutt/muttrc
```
set mail_check = 3600
set copy = no

set from = "foo.bar@gmail.com"
set realname = "Foo Bar"
set envelope_from = yes

# SMTP settings
set smtp_url = "smtps://foo.bar@smtp.gmail.com"
set smtp_pass = "xxxx"
set smtp_authenticators = "plain"

# Remote gmail folders
#set folder = "imaps://imap.gmail.com/"
set spoolfile = "+INBOX"
set postponed = "+[Gmail]/Drafts"
set record = "+[Gmail]/Sent Mail"
set trash = "+[Gmail]/Trash"
```

> Notes:
> * Set `smtp_authenticators` to plain to avoid the "No Authenticators Available" error
> * Enable 2FA and then setup Google [app password](https://support.google.com/accounts/answer/185833?hl=en) as the `smtp_pass` to avoid Google blocking our authentication

## CLI to send email

```
/usr/local/bin/neomutt \
-s "Subject: Line" \
-a "File to attach" \
-- foo.bar2@gmail.com < bodytext.txt
```

> neomutt [manpage](https://neomutt.org/man/neomutt)