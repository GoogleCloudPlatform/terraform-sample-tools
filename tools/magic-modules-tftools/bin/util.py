# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
from time import time

from termcolor import cprint


def show_warning(text):
    cprint(text=str(text + "\n"), color="red")


def show_title(text):
    cprint(str(text + "\n"), color="blue", attrs=["bold"])


def show_heading(text):
    cprint(str(text + "\n"), color="cyan")


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        line = "---------------------[starting - {}]---------------------"
        logging.debug(line.format(func.__name__))
        result = func(*args, **kwargs)
        t2 = time()
        logging.info(f"Function {func.__name__!r} executed in {(t2 - t1):.4f}s")
        line = "---------------------[ending - {}]---------------------"
        return result

    return wrap_func
