# resource "github_repository" "name" {
#   name = ""
#   description = ""
# }

# resource "github_branch" "main" {
#   repository = github_repository.name.name
#   branch = "main"
# }

resource "github_repository_webhook" "my_hook" {
    repository = var.repository_name
    events     = ["push"]
    configuration {
        url          = "http://${linode_instance.HW_Instance.ip_address}:5000/webhook"
        content_type = "json"
    }  
}

resource "linode_instance" "HW_Instance" {
    region = "us-central"
    type = "g6-nanode-1"
    label = "HW_Instance"
    image = "linode/ubuntu24.04"
    root_pass = var.root_pass
    authorized_keys = var.ssh_key
}
