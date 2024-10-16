# Contributors Guide

To be able to contribute, all you need is to have [prerequisites from readme](./README.md#prerequisites) installed. The other tool that I'm using is the [pre-commit](https://pre-commit.com/), it can save a lot of time. And here is the order of what you need.

1. A cup of coffee
2. A computer running Linux/MacOs
3. An IDE of choice, I prefer VSCode
4. Install prerequisites
5. Then execute the following:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r ./api/requirements.txt
```
6. Develop new feature with all tests and docs
7. Then `pre-commit run --all`
8. Run the other tests
```bash
./scripts/startup.sh
./scripts/integration-test.sh
./scripts/performance-test.sh
```
9. Commit the changes
10. Submit the Pull requests
11. You reached to the next level of awesomenewss.
12. Don't forget to run `./scripts/cleanup.sh`.
