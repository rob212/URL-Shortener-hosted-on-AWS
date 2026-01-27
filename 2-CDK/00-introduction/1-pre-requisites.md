# Pre-requisites: Setting Up Your Cloud Command Center

Before we can write code that builds infrastructure, we need to install the tools that translate our Python instructions into AWS resources. 

In this iteration, we are using **mise** (pronounced "meez") to manage our runtimes. It allows us to manage Node.js and Python versions simultaneously, ensuring everyone working on this project uses the exact same environment.

---

## 1. Install mise (The Polyglot Tool Manager)

[**mise**](https://mise.jdx.dev/getting-started.html) is a tool for managing multiple versions of languages on your machine.

### For macOS/Linux:

I advise you install via [Homebrew](https://brew.sh/). 

```bash
brew install mise
```

**Activation:**
You must "hook" mise into your shell so it can switch versions automatically. For the default macOS terminal (Zsh), run:

```bash
echo 'eval "$(mise activate zsh)"' >> ~/.zshrc
source ~/.zshrc
```

### 2. Install Node & Python:
If they aren't already installed on your machine, we will create a mise.toml file in the root of your 2-CDK directory. This file acts as a manifest for your development environment.

```bash
mise use node@22
mise use python@3.12
```

#### What happened?

Mise created a mise.toml file. It looks like this:
```toml
[tools]
node = "22"
python = "3.12"
```

Now, whenever you enter this directory, mise will automatically switch your terminal to these versions. If you cd .. out of the folder, your terminal returns to your system defaults.

### 3. Install the AWS CLI & CDK

The tools that talk to the cloud should be installed as system-wide utilities.

1. AWS CLI: Follow the [Official AWS CLI Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). (Version 2)

2. AWS CDK: Since Node is now active via mise, install the CDK orchestrator:

```bash
npm install -g aws-cdk
```

