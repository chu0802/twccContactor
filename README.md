# twccContactor
A python script handling twccli much easier.

## Dependencies
It's a script specialized for contact with twccli, thus, please make sure you've installed twccli via pip. (See [here](https://man.twcc.ai/@twccdocs/doc-cli-main-zh/)).

```
pip install TWCC-CLI
```

## Installation

twccContactor has been an executable. Thus, it is highly recommended to install it in your local bin directory. (e.g., `~/.local/bin`)

1. (Optional) If `~/.local/bin` doesn't exist, or it hasn't been added in your `PATH`.
  ```
  mkdir ~/.local/bin
  echo 'PATH="~/.local/bin":$PATH' >> ~/.bashrc
  source ~/.bashrc
  ```
2. Download twccContactor to `~/.local/bin`, and set an alias to easily using it.
  ```
  git clone https://github.com/chu0802/twccContactor
  cp twcc.py ~/.local/bin
  rm -rf twccContactor
  echo 'alias twcc="twcc.py"' >> ~/.bashrc
  source ~/.bashrc
  ```

## Usage

twccContactor currently support 4 command.

* Create a new container (`mk`)
* List all existing containers (`ls`)
* Connect to a container (`cnt`)
* Remove a container (`rm`)

### Create a new container

By default, it will create a container with `pytorch 1.8.0`, user can only set the name, and the number of gpu to the container.

#### Command

```
twcc mk -n <name> -g <#gpu>
```

### List all existing containers

This command is equivalent to `twccli ls ccs`.

```
twcc ls
```

### Connect to a container

One of the most important features for **twccContactor**, directly connect to a container by the given name, or the site-id.

If the given container doesn't exist, twccContactor will automatically create one, waiting until the container is ready, and connect to it.

#### Command

```
$(twcc [-n <name> | -s <sid>] -g <#gpu>)
```

or 

```
$(twcc cnt [-n <name> | -s <sid>] <#gpu>)
```

*Note: To avoid unexpected exceptions when directly calling `ssh` in python script, twccContactor will only print the ssh-command to STDOUT. Thus, to execute it, one should use `$(twcc cnt ...)`, instead of directly calling `twcc cnt ...`.*

*Note: When there're multiple containers with the same name, by default, twccContactor will connect to the first container. To selecting a specific one, please first list all containers' information, and selecting it according to the corresponding site-id.*

### Remove a container

Remove a container by given either the name, or the site-id.

#### Command

```
twcc rm [-n <name | -s <sid>]
```

*Note: When there're multiple containers with the same name, by default, twccContactor will delete the first container. To remove a specific one, please first list all containers' information, and selecting it according to the corresponding site-id.*
