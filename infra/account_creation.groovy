properties([
    parameters([
        string(name: 'ROOT_OU_ID', defaultValue: 'r-i68s', description: 'Id of the root OU'),
        string(name: 'SANDBOX_OU_ID', defaultValue: 'ou-i68s-ggbxakm3', description: 'Id of the Sandbox OU'),
        string(name: 'FINAL_ACCOUNT_DATA_BUCKET', defaultValue: 'sandbox-accounts-details', description: 'S3 bucket to store final account data'),
        string(name: 'SES_VERIFIED_SOURCE_EMAIL', defaultValue: 'madhurgupta590+ses@gmail.com', description: 'Email address verified in SES for sending emails'),
    ])
])


node {
    env.PYTHONPATH = "${WORKSPACE}/src"

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
                dir('src/account_creation') {
                    sh "python3 run.py --root-ou-id ${params.ROOT_OU_ID} --sandbox-ou-id ${params.SANDBOX_OU_ID} --final-account-data-bucket ${params.FINAL_ACCOUNT_DATA_BUCKET} --source-email ${params.SES_VERIFIED_SOURCE_EMAIL}"
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
