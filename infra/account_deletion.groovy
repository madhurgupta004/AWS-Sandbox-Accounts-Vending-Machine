properties([
    parameters([
        string(name: 'ACCOUNT_ID', description: 'ID of the account to delete'),
        ])
])

node {
    env.PYTHONPATH = "${WORKSPACE}/src/account_deletion"

    try {
        stage('Checkout') {
            checkout scm
        }

        stage('Run Python Script') {
            withCredentials([[
                $class: 'AmazonWebServicesCredentialsBinding',
                credentialsId: 'my_aws_account',
                accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
            ]]) {
                dir('src/account_deletion') {
                    sh "python3 run.py --account-id ${params.ACCOUNT_ID}"
                }
            }
        }
    } catch (Exception e) {
        echo 'Pipeline failed!'
        throw e
    } finally {
        cleanWs()
    }
}
