The [official tutorial](https://docs.aws.amazon.com/glue/latest/dg/dev-endpoint-tutorial-repl.html) describes how to invoke a REPL shell from a terminal, and this guide supplements the last mile -- calling the REPL shell from within VS Code.

- [Generate SSH keypair](#generate-ssh-keypair)
- [AWS Glue development endpoint](#aws-glue-development-endpoint)
- [VS Code](#vs-code)
  - [Keyboard shortcut to run selected text](#keyboard-shortcut-to-run-selected-text)
  - [Terminal settings](#terminal-settings)
  - [Final touch](#final-touch)

# Generate SSH keypair

macOS:
```
ssh-keygen


Generating public/private rsa key pair.
Enter file in which to save the key (/Users/xxxxx/.ssh/id_rsa): /Users/xxxxx/Desktop/aws-glue.pem
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /Users/xxxxx/Desktop/aws-glue.pem.
Your public key has been saved in /Users/xxxxx/Desktop/aws-glue.pem.pub.
```

Windows: use PuTTYgen

# AWS Glue development endpoint

1. In the [AWS Glue console](https://console.aws.amazon.com/glue/home), under the navigation menu on the left, click **Dev endpoints**
2. Click **Add endpoint**
   * Development endpoint name: *dev*
   * IAM role: Create a new role with
     * AmazonS3FullAccess
     * AWSGlueServiceNotebookRole
   * Worker type: *Standard* (default) 
   * DPU: *2* (minimum)
   * Catalog options: *Use Glue data catalog as the Hive metastore*
   * Skip networking information
     * To secure the dev endpoint in a VPC, select *Choose a connection*. 
   * Add an SSH public key: *Upload the aws-glue.pem.pub file* 
3. When the provisioning has finished, open the endpoint details and copy the value of **SSH to Python REPL**
```
ssh -i <private-key.pem> glue@xxxxx.amazonaws.com -t gluepyspark3
```

# VS Code

## Keyboard shortcut to run selected text

* Open keyboard shortcuts settings (Ctrl+K+S or Cmd+K+S)
* Search for `workbench.action.terminal.runSelectedText`
* Map with an unused binding, such as Ctrl+Shift+Enter or Cmd+Shift+Enter

## Terminal settings

* Create a new file named **test.py**
* Open a new terminal (**Terminal** > **New terminal**)
* Issue the SSH to Python REPL command copied above and we'll see the welcome banner
  * Replace <private-key.pem> with your private key file
```Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 2.4.3
      /_/

Using Python version 3.6.10 (default, Feb 10 2020 19:55:14)
SparkSession available as 'spark'.
```

## Final touch

* Set the logging level to ERROR to avoid frequent interruption by warning messages
```
sc.setLogLevel("ERROR")
```
* In the editor of the **test.py** file, write a few lines of code:
```python
spark.version

spark.sql("SHOW DATABASES").show()
```
* Select only the first line, and press the hotkey (e.g., Ctrl+Shift+Enter)
* We should see the line is being issued to the remote Glue dev endpoing, and the version number is displayed in the terminal

> Note that the key binding `Shift+Enter` is by default assigned to run the selected lines in a new Python shell, and not the SSH tunnel that we have connected to the Glue dev endpoing.